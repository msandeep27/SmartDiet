from flask import render_template, jsonify, Flask, redirect, url_for, request
from app import app
import random
import os
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
import io
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from keras.models import load_model

@app.route('/')

#disease_list = ['Atelectasis', 'Consolidation', 'Infiltration', 'Pneumothorax', 'Edema', 'Emphysema', \
                  # 'Fibrosis', 'Effusion', 'Pneumonia', 'Pleural_Thickening', 'Cardiomegaly', 'Nodule', 'Mass', \
                  # 'Hernia']

@app.route('/upload')
def upload_file2():
   return render_template('index.html')


model = None
MODEL_PATH = './models/'
MODEL_FILE_NAME = 'ResNet_model_weights.h5'
#MODEL_FILE_NAME = 'MobileNet_model_weights.h5'
MODEL_CLASS_FILE_NAME = 'ResNet_classLabelMap.npy'
#MODEL_CLASS_FILE_NAME = 'MobileNet_classLabelMap.npy'
MODEL_CLASS_MAPP = {}

def retrieve_model():
    # load the pre-trained Keras model (here we are using a model
    # pre-trained on ImageNet and provided by Keras, but you can
    # substitute in your own networks just as easily)
    
    if not os.path.exists(MODEL_PATH):
        os.mkdir(MODEL_PATH)
        print("Directory " , MODEL_PATH ,  " Created ")
    else:    
        print("Directory " , MODEL_PATH ,  " already exists")
    
    modelFilePath = MODEL_PATH + MODEL_FILE_NAME

    dictPath = MODEL_PATH + MODEL_CLASS_FILE_NAME
    global MODEL_CLASS_MAPP
    MODEL_CLASS_MAPP = np.load(dictPath, allow_pickle=True).item()

    global model
    model = load_model(modelFilePath)
    print("Retrieving Model  >> "+modelFilePath)
    model.summary()

    #model = ResNet50(weights="imagenet")
    model._make_predict_function()
    



def prepare_image_old(image, target):
    # if the image mode is not RGB, convert it
    if image.mode != "RGB":
        image = image.convert("RGB")

    # resize the input image and preprocess it
    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)

    # return the processed image
    return image

def prepare_image(path, target):
    # if the image mode is not RGB, convert it
    img = image.load_img(path, target_size=target)

    # resize the input image and preprocess it
    #image = image.resize(target)
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = imagenet_utils.preprocess_input(img)

    # return the processed image
    return img

def model_predict(image, model):
    data = {"success": False, "Prediction": "None"}
    data["predictions"] = []

    preds = model.predict(image)
    
    for class_index in range(len(MODEL_CLASS_MAPP)):
        class_label = MODEL_CLASS_MAPP[class_index]
        r = {"Label": class_label, "Probability": float(preds[0][class_index])}
        data["predictions"].append(r) 
        pass

    prediction=np.argmax(preds,axis=1)
    data["Prediction"] = MODEL_CLASS_MAPP[prediction[0]]

    data["success"] = True


    #results = imagenet_utils.decode_predictions(preds)
    #data["predictions"] = []

    #for (imagenetID, label, prob) in results[0]:
    #            r = {"label": label, "probability": float(prob)}
    #            data["predictions"].append(r)

    #data["success"] = True
    
    return data

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   retrieve_model()
   if request.method == 'POST':
      f = request.files['file']
      path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
      #print(path)
      #image = Image.open(path)

      # preprocess the image and prepare it for classification
      image = prepare_image(path, target=(224, 224))

      # classify the input image and then return prediction data
            
      preds_decoded = model_predict(image, model)
      #model= ResNet50(weights='imagenet')
      #img = image.load_img(path, target_size=(224,224))
      #x = image.img_to_array(img)
      #x = np.expand_dims(x, axis=0)
      #x = preprocess_input(x)
      #preds = model.predict(x)
      #preds_decoded = decode_predictions(preds, top=3)[0] 
      print("Prediction >> "+str(preds_decoded))
      #f.save(path)
      return render_template('uploaded.html', title='Success', predictions=preds_decoded, user_image=f.filename)


@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/map')
def map():
    return render_template('map.html', title='Map')


@app.route('/map/refresh', methods=['POST'])
def map_refresh():
    points = [(random.uniform(48.8434100, 48.8634100),
               random.uniform(2.3388000, 2.3588000))
              for _ in range(random.randint(2, 9))]
    return jsonify({'points': points})


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact')


if __name__ == "__main__":

    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    retrieve_model()
