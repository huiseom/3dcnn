# from __future__ import print_function
import keras
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv3D, MaxPooling3D, GlobalAveragePooling3D
from keras.optimizers import SGD


'''
1. 전체 구조 
    conv. layer: 8개
    max pooling: 5개
    Fully conv. layer: 2개

2. number of filters
    conv1: 64
    conv2: 128
    conv3: 256
    conv4: 512
    conv5: 512
    
3. kernel size
    conv. layer: (3,3,3)
    max pooling except for the 1st pooling: (2,2,2) for 1 stride
    1st max pooling: (2,2,1) for 2 stride
'''

def modelConstructor():
    model = Sequential()

    # 1st conv. layer and pooling
    model.add(Conv3D(64, kernel_size=(3, 3, 3), activation='relu', strides=1, input_shape=(16, 240, 320, 3), padding="same"))
    model.add(MaxPooling3D(strides=2,pool_size=(2,2,1)))


    # 2nd conv. layer and pooling
    model.add(Conv3D(128, kernel_size=(3, 3, 3), strides=1, activation='relu', padding="same"))
    model.add(MaxPooling3D(strides=1, pool_size=(2, 2, 2)))


    # 3rd conv. layer a,b and pooling
    model.add(Conv3D(256, kernel_size=(3, 3, 3),strides=1, activation='relu',padding="same"))
    model.add(Conv3D(256, kernel_size=(3, 3, 3), strides=1,activation='relu',padding="same"))
    model.add(MaxPooling3D(strides=1, pool_size=(2, 2, 2)))

    # 4th conv. layer a,b and pooling
    model.add(Conv3D(512, kernel_size=(3, 3, 3), strides=1,activation='relu',padding="same"))
    model.add(Conv3D(512, kernel_size=(3, 3, 3), strides=1,activation='relu',padding="same"))
    model.add(MaxPooling3D(strides=1, pool_size=(2, 2, 2)))


    # 5th conv. layer a,b and pooling
    model.add(Conv3D(512, kernel_size=(3, 3, 3), strides=1,activation='relu',padding="same"))
    model.add(Conv3D(512, kernel_size=(3, 3, 3), strides=1,activation='relu',padding="same"))
    model.add(MaxPooling3D(strides=1, pool_size=(2, 2, 2)))

    # adding a conv. layer: filter = 3 by 3, stride = 1, pad =1, channel= 1024
    model.add(Conv3D(1023, kernel_size=(3, 3, 3), strides=1, activation='relu', padding="same"))

    # global average pooling
    model.add(GlobalAveragePooling3D())

    model.add(Dense(2, activation='softmax'))
    model.summary()

    optimizerAdam = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)

    model.compile(optimizer=optimizerAdam,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model





def modelTrain(trainData, trainLabel,epch, batch):
    model = modelConstructor()

    # tb_hist = keras.callbacks.TensorBoard(log_dir='./graph', histogram_freq=0, write_graph=True, write_images=True)

    # print(type(trainData),np.shape(trainData),np.shape(trainLabel))

    hist = model.fit(trainData, trainLabel, epochs=epch, verbose= 2, batch_size=batch)

    #
    # print(hist.history['loss'])
    # print(hist.history['acc'])
    # print(hist.history['val_loss'])
    # print(hist.history['val_acc'])


    return hist

def modelEvaluation(model, testData, testLabel):

    test_loss, test_acc = model.evaluate(testData, testLabel)
    print("test acc. is ", test_acc)

# modelConstructor()

