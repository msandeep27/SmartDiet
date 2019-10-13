import pandas as pd
import numpy as np
import os
from keras.models import Sequential, Model
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers, optimizers
from keras.applications.resnet50 import ResNet50
from keras.applications import MobileNet
from keras.optimizers import SGD, Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def load_dataFrame(targetImageHeight, targetImageWidth, batchSize):
    trainDf = pd.read_csv('./MLTrain/DataSets/TrainFoodDataSet.csv')  
    testDf = pd.read_csv('./MLTrain/DataSets/TestFoodDataSet.csv')  
    fullDf = pd.read_csv('./MLTrain/DataSets/FullFoodDataSet.csv')  

    class_list = fullDf['Class'].unique().tolist()

    datagen=ImageDataGenerator(rescale=1./255.,validation_split=0.25)
    train_generator=datagen.flow_from_dataframe(
        dataframe=trainDf,
        directory="",
        x_col="ImagePath",
        y_col="Class",
        subset="training",
        batch_size=batchSize,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(targetImageHeight,targetImageWidth))
    valid_generator=datagen.flow_from_dataframe(
        dataframe=trainDf,
        directory="",
        x_col="ImagePath",
        y_col="Class",
        subset="validation",
        batch_size=batchSize,
        seed=42,
        shuffle=True,
        class_mode="categorical",
        target_size=(targetImageHeight,targetImageWidth))

    test_datagen=ImageDataGenerator(rescale=1./255.)
    test_generator=test_datagen.flow_from_dataframe(
        dataframe=testDf,
        directory="",
        x_col="ImagePath",
        y_col=None,
        batch_size=batchSize,
        seed=42,
        shuffle=False,
        class_mode=None,
        target_size=(targetImageHeight,targetImageWidth))


    label_map = (train_generator.class_indices)
    label_map = dict((v,k) for k,v in label_map.items()) #flip k,v

    return class_list, train_generator, valid_generator, test_generator, label_map




def get_base_model(model_name):
    imgHeight = 0
    imgWidth = 0
    if model_name == "ResNet":
        imgHeight = 224
        imgWidth = 224
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(imgHeight, imgWidth, 3))
    elif model_name == "MobileNet":
        imgHeight = 224
        imgWidth = 224        
        base_model=MobileNet(weights='imagenet',include_top=False, input_shape=(imgHeight, imgWidth, 3)) #imports the mobilenet model and discards the last 1000 neuron layer.        
    else:
        imgHeight = 224
        imgWidth = 224
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(imgHeight, imgWidth, 3))

    return base_model, imgHeight, imgWidth




    

def build_finetune_model(base_model, dropout, fc_layers, num_classes, imgHeight, imgWidth):    
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = Flatten()(x)
    for fc in fc_layers:
        # New FC layer, random init
        x = Dense(fc, activation='relu')(x) 
        x = Dropout(dropout)(x)

    # New softmax layer
    predictions = Dense(num_classes, activation='softmax')(x) 
    
    finetune_model = Model(inputs=base_model.input, outputs=predictions)    
    adam = Adam(lr=0.00001)
    finetune_model.compile(adam, loss='categorical_crossentropy', metrics=['accuracy'])

    return finetune_model




checkpointPath = "./checkpoints/"
if not os.path.exists(checkpointPath):
    os.mkdir(checkpointPath)

model_name = "MobileNet"
class_list, train_generator, valid_generator, test_generator, label_map = load_dataFrame(224,224,32)
np.save('./models/' + model_name + '_classLabelMap.npy', label_map) 

FC_LAYERS = [512,256]
dropout = 0.2
base_model, imgHeight, imgWidth = get_base_model(model_name)
finetune_model = build_finetune_model(base_model, 0.5, FC_LAYERS, len(class_list), imgHeight, imgWidth)


filepath="./checkpoints/" + model_name + "_model_weights.h5"
checkpoint = ModelCheckpoint(filepath, monitor=["acc"], verbose=1, mode='max')
callbacks_list = [checkpoint]

NUM_EPOCHS = 10
STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
STEP_SIZE_TEST=test_generator.n//test_generator.batch_size
history = finetune_model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=NUM_EPOCHS,
                    shuffle=True,
                    callbacks=callbacks_list)





