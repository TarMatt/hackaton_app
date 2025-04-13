from PIL import Image
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from io import BytesIO
import torch

from torchvision import transforms
from torchvision.ops import nms
import streamlit as st

# Functions -------------------------------------------------------------------------------------------------------------
from torchvision.models.detection import ssdlite320_mobilenet_v3_large,SSDLite320_MobileNet_V3_Large_Weights

# Function to assign labels and others

def detect_animals(data,model,weights,box_threshold:int): 
    
    with torch.no_grad():
        
        predictions = model(data)
                    
        apply_nms = lambda pred: nms(pred['boxes'],pred['scores'],iou_threshold=0.4)

        nms_pred = list(map(lambda pred: {
            'boxes':pred['boxes'][apply_nms(pred)],
            'labels':pred['labels'][apply_nms(pred)],
            'scores':pred['scores'][apply_nms(pred)]
        },predictions))
        
        img_res = nms_pred[0]
            
        if img_res['boxes'].detach().numpy().size==0:
            box=None
            label=None
            confidence=None
            objects=[{'box':box,'label':label,'confidence':confidence}]
        else:
            boxes = img_res['boxes']
            labels = img_res["labels"]
            confidences= img_res['scores'].detach().numpy()

            objects=[]
            for idx,box in enumerate(boxes):
                score=float(confidences[idx])
                if score >= box_threshold:
                
                    box=list(map(int,box))

                    oggetto={'box':box,'label':labels[idx],'confidence':round(score,3)}

                    objects.append(oggetto)
                else: 
                    continue
                
            if len(objects)==0:
                box=None
                label=None
                confidence=None
                objects=[{'box':box,'label':label,'confidence':confidence}]
                
            results=objects
            
            for object in results:
                idx=object['label']
                if idx!=None:
                    object['label']=weights.meta["categories"][idx]
            
        return results
    

#------------------------------------------------------------------------------------------------------------------------------


weights = SSDLite320_MobileNet_V3_Large_Weights.DEFAULT
model = ssdlite320_mobilenet_v3_large(weights=weights)
model.eval()


app = FastAPI()

@app.get("/")
def read_root(text: str = ""):
    if not text:
        return f"Append ?text=help for a description of the backend"
    if text == "help":
        description = "I'm working on it"
        return description


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    file_img = await file.read()
    image = Image.open(BytesIO(file_img)).convert("RGB")
    transform = transforms.ToTensor()
    data = transform(image).unsqueeze(0)
    results = detect_animals(data,model=model,weights=weights,box_threshold=0.5)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="localhost", port=8000, reload=True)