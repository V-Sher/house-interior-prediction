# import os
# import io
import base64
import numpy as np
from flask import Flask, render_template, request
from PIL import Image
from tensorflow.keras.models import load_model
# from utils import model_config

IMG_SHAPE = (224,224)
CLASSES = ["Modern", "Old", "Neutral"]

# # project home directory
# basedir = os.path.abspath(os.path.dirname(__file__))

# # loading trained model
# model_fpath = os.path.join(basedir, 'output', 'house.model')
model = load_model('house.model')

# define this is a flask app
app = Flask(__name__)

# create a dict to populate the form; must be used when rendering the index.html
myage = np.random.randint(10,100)
personal_details = {'name': "Boooooooo Sher Reddy", 
                    'age': myage}

# basic first page
@app.route('/')
def sayhello():
    return render_template('index.html', personal_details=personal_details)

@app.route('/dummy', methods=['POST'])
def dummy():
    f = request.files['img']
    fpath = getfpath(f)
    file = Image.open(f)
    file_shape = np.asarray(file).shape
    
    #### PREDICTION STARTS HERE ####
    
    # resize image to (224,224) if needed
    if file.size != IMG_SHAPE:
        file = file.resize(IMG_SHAPE)
        file_shape = np.asarray(file).shape
    
    # pass the image through the network to obtain our predictions
    preds = model.predict(np.expand_dims(file, axis=0))[0]
    i = np.argmax(preds)
    label = CLASSES[i]
    prob = preds[i]
    
    pred_output={
    'img_size': file_shape,
    'label': label,
    'probability': np.round(prob*100,2)
    }  
    
    return render_template('index.html', 
                           personal_details=personal_details, 
                           img_shape=file_shape,
                           user_image=fpath,
                        #    pred_output=pred_output
                           )

# # the name you give here in route will be reflected in URL
# @app.route('/disp_size_myimg', methods=['POST'])
# def disp_size():
#     f = request.files['img']  
#     fpath = getfpath(f) # need this to display img in < img src=???>
#     file = Image.open(f)
#     file_shape = np.asarray(file).shape
    
#     #### PREDICTION STARTS HERE ####
    
#     # resize image to (224,224) if needed
#     if file.size != model_config.IMG_SHAPE:
#         file = file.resize(model_config.IMG_SHAPE)
#         file_shape = np.asarray(file).shape
        
#     # pass the image through the network to obtain our predictions
#     preds = model.predict(np.expand_dims(file, axis=0))[0]
#     i = np.argmax(preds)
#     label = model_config.CLASSES[i]
#     prob = preds[i]
    
#     pred_output={
#         'img_size': file_shape,
#         'label': label,
#         'probability': np.round(prob*100,2)
#     }        
#     return render_template('index.html', 
#                            personal_details=personal_details, 
#                            pred_output=pred_output,
#                            user_image=fpath) # the html file must contain placeholders for {{user_image}}
    

def getfpath(img) -> str:
    # convert to bases64
    data = img.read()              # get data from file (BytesIO)
    data = base64.b64encode(data)  # convert to base64 as bytes
    data = data.decode()           # convert bytes to string

    # convert to <img> with embed image
    fpath = "data:image/png;base64,{}".format(data)
    
    return fpath

if __name__=="__main__":
    app.run(debug=True)



