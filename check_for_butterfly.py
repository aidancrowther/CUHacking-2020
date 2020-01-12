from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, ConvLSTM2D, LSTM, Reshape, Activation
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K
import os, sys
import cv2
import numpy as np

#Setup keras callbacks for checkpointing, earlystopping, and tensorboard
filepath="weights-best-finder.hdf5"
num_classes = 2

# input image dimensions
img_rows, img_cols = 400, 400

input_shape = (img_rows, img_cols, 3)

def getClass(img):
    print(img)
    image = cv2.imread(img)

    if image is None or image.shape[0] < 400 or image.shape[1] < 400 : return None
    
    image = cv2.resize(image, (400, 400))
    image = np.array([image])
    image.astype('float32')
    np.true_divide(image, 255)

    # convert class vectors to binary class matrices

    result = model.predict(image).tolist()

    return result[0]

model = Sequential()
model.add(Conv2D(8, kernel_size=(8, 8), strides=(1, 1),
                    input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(4, 4)))
model.add(Conv2D(16, (4, 4)))
model.add(Dropout(0.3))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3)))
model.add(Dropout(0.3))
model.add(Activation("relu"))
model.add(Conv2D(32, (2, 2)))
model.add(Dropout(0.3))
model.add(Activation("relu"))

model.add(Reshape(target_shape=(1936, 32)))
ConvLSTM2D(filters=8, kernel_size=(3, 3), input_shape=(None, 110, 64), padding='same', return_sequences=True,  stateful = True)
model.add(LSTM(64, return_sequences=True, input_shape=(110, 64)))
model.add(Dropout(0.3))
model.add(Activation("relu"))
model.add(LSTM(32, activation='relu', return_sequences=True))
model.add(Flatten())
model.add(Dense(1024))
model.add(Dropout(0.3))
model.add(Activation("relu"))
model.add(Dense(16, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))

model.load_weights(filepath)

model.compile(loss=keras.losses.categorical_crossentropy,
    optimizer="adam",
    metrics=['accuracy'])