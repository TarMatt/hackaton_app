from PIL import Image
import matplotlib.pyplot as plt
import requests
import streamlit as st

def plot_img(image,results):

    image_shape= (image.size[0],image.size[1])
    # Create the figure
    plt.figure(figsize=(10, 10))
    plt.imshow(image)

    #Set what to do in case of 'empty image'
    if results==[{'box':None,'label':None,'confidence':None}]:
        plt.axis(False)
        return
        
    #Set what to do in case of one or multiple objects
    else:
        #Iterate over the number of objects to plot multiple boxes
        for obj in results:
            #Define the coordinates of the box
            x1=int(obj['box'][0])
            x2=int(obj['box'][2])
            y1=int(obj['box'][1])
            y2=int(obj['box'][3])

            # Adjust min and max dimensions
            if x1 < 0:
                x1 = 0
            if x2 > image_shape[0]:
                x2 = image_shape[0]
            if y1 < 0:
                y1 = 0
            if y2 > image_shape[1]:
                y2 = image_shape[1]

            #Define the label and the confidence associate to that box
            label=obj['label']
            confidence=obj['confidence']

            #Plot the rectangle, the label and the confidence associate to the object
            ##Set the danger color
            if label=='bear':
                color ='red'
            else:
                color='blue'
            plt.gca().add_patch(plt.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=1.5, edgecolor=color, facecolor='none'))
            plt.text(x2-5,y1, label +'__' + f'{confidence:.3f}', color='black', fontsize=12, ha='right', va='bottom',
                        bbox=dict(facecolor=color, alpha=0.7, edgecolor='none', boxstyle='round,pad=0.3'))
            plt.axis(False)
           
    return plt
 
 #--------------------------------------------------------------------------------------------------------------------------------
   

def app():
    
    st.set_page_config(layout="wide")
    # Set the title of the app
    st.title("Wildlife detection using camera traps 🔍")

    # Upload image
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        col1, col2 = st.columns([2, 1])
        

        with col1:
            # Display the uploaded image
            image = Image.open(uploaded_file)
           
            image_placeholder = st.empty()
            image_placeholder.image(image, caption="Uploaded Image", use_container_width=True)
        
        with col2:
            # Make prediction
            if st.button('DETECT ANIMALS'):
                
                backend_url = 'https://det-backendv2-497430069448.us-central1.run.app/predict/'
                files = {"file": uploaded_file.getvalue()}
                results = requests.post(backend_url, files=files).json()

                image_placeholder.pyplot(plot_img(image,results))
                
                therebear = [obj['label'] for obj in results if obj['label']=='bear']

                if len(therebear)>=1:
                    st.markdown("<h3 style='color: red;'> ‼️ATTENTION‼️ <br>ONE OR MORE BEAR DETECTED 🐻</h3>", unsafe_allow_html=True)

                else:
                    st.markdown("<h3 style='color: white; '> EVERYTHING'S FINE 👍🏻<br> NO THREATS DETECTED</h3>",unsafe_allow_html=True)

                
                for object in results:
                    st.write(f"Detected class:_{object['label']}--Confidence score:_{object['confidence']}")      

if __name__ == "__main__":
    app()