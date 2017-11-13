from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.utils import np_utils
from PIL import Image
import numpy as np
import os, glob

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

root_dir = "./simulation/"
categories = ["goldenretriever", "husky", "pomeranian", "poodle", "welshcorgi"]
nb_classes = len(categories)
image_size = 64

def main(model, filename):

    # X_train, X_test, y_train, y_test = np.load("./image/dog.npy")
    #
    # X_train = X_train.astype("float") / 256
    # X_test = X_test.astype("float") / 256
    # y_train = np_utils.to_categorical(y_train, nb_classes)
    # y_test = np_utils.to_categorical(y_test, nb_classes)


    X = []
    files = []
    image_dir = root_dir
    # files = glob.glob(image_dir + "/*.jpg")
    # files.extend(glob.glob(image_dir + "/*.png"))
    files.append(filename)
    for i, fname in enumerate(files):
        img = Image.open(fname)
        img = img.convert("RGB")
        img = img.resize((image_size, image_size))
        data = np.asarray(img)
        X.append(data)
    X = np.array(X)

    # model = build_model(X.shape[1:])
    # model.load_weights('./model/dog-model.hdf5')

    pre = model.predict(X)
    for i, p in enumerate(pre):
        y = p.argmax()
        print(categories[y])

    return categories[y]

def build_model(in_shape):

    model = Sequential()

    model.add(Convolution2D(32, 3, 3, border_mode='same', input_shape=in_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, 3, 3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))

    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    return model

def model_train(X, y):

    model = build_model(X.shape[1:])

    hdf5_file = "./model/dog-model.hdf5"
    model.load_weights(hdf5_file)

    return model

if __name__ == "__main__":
    main()









