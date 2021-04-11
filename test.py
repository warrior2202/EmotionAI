import streamlit as st
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import PIL
from PIL import Image, ImageOps
import seaborn as sns
import pickle
from PIL import *
import cv2
with open('detection.json', 'r') as json_file:
    json_savedModel= json_file.read()

with open('emotion.json', 'r') as json_file:
    json_savedModel2= json_file.read()
    
    
# load the model architecture 
model_1_facialKeyPoints = tf.keras.models.model_from_json(json_savedModel)
model_1_facialKeyPoints.load_weights('weights_keypoint.hdf5')
adam = tf.keras.optimizers.Adam(learning_rate=0.0001, beta_1=0.9, beta_2=0.999, amsgrad=False)
model_1_facialKeyPoints.compile(loss="mean_squared_error", optimizer= adam , metrics = ['accuracy'])
model_2_emotion = tf.keras.models.model_from_json(json_savedModel2)
model_2_emotion.load_weights('weights_emotions.hdf5')
model_2_emotion.compile(optimizer = "Adam", loss = "categorical_crossentropy", metrics = ["accuracy"])
def main():
    st.set_option('deprecation.showfileUploaderEncoding', False)

    st.title("Emotion Ai")
    st.write("")

    




file_up = st.file_uploader("Upload an image", type="jpg")



def predict(X_test):

  # Making prediction from the keypoint model
  df_predict = model_1_facialKeyPoints.predict(X_test)

  # Making prediction from the emotion model
  df_emotion = np.argmax(model_2_emotion.predict(X_test), axis=-1)

  # Reshaping array from (856,) to (856,1)
  df_emotion = np.expand_dims(df_emotion, axis = 1)

  # Converting the predictions into a dataframe
  df_predict = pd.DataFrame(df_predict)

  # Adding emotion into the predicted dataframe
  df_predict['emotion'] = df_emotion

  return df_predict

if st.button("Predict"):
       img = Image.open(file_up)
       im2 = ImageOps.grayscale(img)
       im3 = im2.resize((96,96), Image.ANTIALIAS)
       im3.save('somepic.jpg')
       gray_img = cv2.imread('somepic.jpg', cv2.IMREAD_GRAYSCALE)
       dummy = gray_img
       dummy = np.stack(dummy, axis = 0)
       dummy = dummy.reshape(1, 96, 96, 1)
       dummy = dummy/255
       df_predict_test = predict(dummy)
       st.text(df_predict_test['emotion'])



   


if __name__ == '__main__':
	main()