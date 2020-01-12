from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D, ConvLSTM2D, LSTM, Reshape, Activation
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.optimizers import SGD
from keras import backend as K
import os, sys
import cv2
import numpy as np

butterflyPath = 'training/smaller/'
notButterflyPath = 'training/notButterflies/'

#Setup keras callbacks for checkpointing, earlystopping, and tensorboard
filepath="weights-best-finder.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_accuracy', min_delta=0.001, patience=6, verbose=1, mode='auto')
callbacks_list = [earlystop, checkpoint]

batch_size = 8
num_classes = 2
epochs = 10

# input image dimensions
img_rows, img_cols = 400, 400

# the data, split between train and test sets
images = os.listdir( butterflyPath )
count = 0

train_x = []
test_x = []
train_y = []
test_y = []

x = []
y = []

k = 400

images = os.listdir( butterflyPath )
count = 0

print('loading butterflies...')

for image in images:

    if(count % 83 == 0): print('...')

    img = cv2.imread(butterflyPath+image)

    x.append(img)
    y.append(0)

    count += 1

images = os.listdir( notButterflyPath )
count = 0

print('loading not butterflies...')

for image in images:

    if(count % 83 == 0): print('...')

    img = cv2.imread(notButterflyPath+image)

    x.append(img)
    y.append(1)

    count += 1

out_x = []
out_y = []

print(len(x)/2)

for i in range(int(len(x)/2)):
    out_x.append(x[i])
    out_x.append(x[i+int(len(x)/2)])
    out_y.append(y[i])
    out_y.append(y[i+int(len(y)/2)])

x = out_x
y = out_y

for i in range(len(y)):
    if i/len(y) <= 0.1:
        test_x.append(x[i])
        test_y.append(y[i])
    else:
        train_x.append(x[i])
        train_y.append(y[i])

train_x = np.array(train_x)
test_x = np.array(test_x)

train_x.astype('float32')
test_x.astype('float32')

np.true_divide(train_x, 255)
np.true_divide(test_x, 255)

print('train_x shape:', train_x.shape)
print(train_x.shape[0], 'train samples')
print(test_x.shape[0], 'test samples')

input_shape = (img_rows, img_cols, 3)

# convert class vectors to binary class matrices
train_y = keras.utils.to_categorical(train_y, num_classes)
test_y = keras.utils.to_categorical(test_y, num_classes)

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

print(model.summary())

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=SGD(0.01),
              metrics=['accuracy'])

model.fit(train_x, train_y,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          shuffle = True,
          validation_data=(test_x, test_y),
          callbacks=callbacks_list)
score = model.evaluate(test_x, test_y, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])