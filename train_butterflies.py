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

#Setup keras callbacks for checkpointing, earlystopping, and tensorboard
filepath="weights-best-classifier.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
earlystop = EarlyStopping(monitor='val_accuracy', min_delta=0.001, patience=6, verbose=1, mode='auto')
callbacks_list = [earlystop, checkpoint]

classes = []
batch_size = 8
epochs = 20

f = open('species.txt', 'r')
species = f.read().split("\n")
dirs = os.listdir( 'Data/' )

for each in species:
    for dir in dirs:
        if ' '.join(each.split(' - ')) in dir: classes.append(each)

num_classes = len(classes)

data_x = []
data_reserved = []
data_y = []
labels_reserved = []

src = '/clean/'

for dir in dirs:
    species = 'Data/'+dir+src
    species = os.listdir(species)
    count = 0
    for each in species:
        if(count/len(species) < 0.1):
            data_reserved.append('Data/'+dir+src+each)
        else:
            data_x.append('Data/'+dir+src+each)
        count += 1

data_x = np.array(data_x)
np.random.shuffle(data_x)
data_x = data_x.tolist()

for x in data_x:
    for species in classes:
        if ' '.join(species.split(' - ')) in x:
            data_y.append(classes.index(species))
            break

for x in data_reserved:
    for species in classes:
        if ' '.join(species.split(' - ')) in x:
            labels_reserved.append(classes.index(species))
            break
        
print(len(data_x))
print(len(data_y))

print(len(data_reserved))
print(len(labels_reserved))

print('Loading Training')

train_x = []
test_x = []

image = cv2.imread(data_x[0])
image = cv2.resize(image, (400, 400))
image = np.array([image])
image.astype('float32')
np.true_divide(image, 255)

count = 0
for i in range(len(data_x)):
    if count % 1000 == 0: print('...')
    image = cv2.imread(data_x[i])
    image = cv2.resize(image, (400, 400))
    image = np.array([image])
    image.astype('float32')
    np.true_divide(image, 255)

    train_x.append(image[0])
    count += 1

print('Loading Testing')
count = 0
for i in range(len(data_reserved)):
    if count % 100 == 0: print('...')
    image = cv2.imread(data_reserved[i])
    image = cv2.resize(image, (400, 400))
    image = np.array([image])
    image.astype('float32')
    np.true_divide(image, 255)

    test_x.append(image[0])
    count += 1

train_x = np.array(train_x)
test_x = np.array(test_x)
train_y = np.array(data_y)
test_y = np.array(labels_reserved)

print(train_x.shape)
print(test_x.shape)
print(train_y.shape)
print(test_y.shape)

train_y = keras.utils.to_categorical(train_y, num_classes)
test_y = keras.utils.to_categorical(test_y, num_classes)

# input image dimensions
img_rows, img_cols = 400, 400

input_shape = (img_rows, img_cols, 3)

model = Sequential()
model.add(Conv2D(8, kernel_size=(8, 8), strides=(1, 1),
                    input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(4, 4)))
model.add(Conv2D(16, (4, 4)))
model.add(Dropout(0.1))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3)))
model.add(Dropout(0.1))
model.add(Activation("relu"))

model.add(Reshape(target_shape=(2025, 32)))
ConvLSTM2D(filters=8, kernel_size=(3, 3), input_shape=(None, 110, 64), padding='same', return_sequences=True,  stateful = True)
model.add(LSTM(64, return_sequences=True, input_shape=(110, 64)))
model.add(Dropout(0.2))
model.add(Activation("relu"))
model.add(LSTM(32, activation='relu', return_sequences=True))
model.add(Flatten())
model.add(Dense(256))
model.add(Dropout(0.2))
model.add(Activation("relu"))
model.add(Dense(32, activation='relu'))
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