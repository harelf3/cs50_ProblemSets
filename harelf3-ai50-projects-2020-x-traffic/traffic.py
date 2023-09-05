
import cv2
import numpy as np
import os
import sys
from scipy.sparse.lil import _prepare_index_for_memoryview
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
# NUM_CATEGORIES = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])
    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()
    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=1)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    ###
    # so we gonna loop 0-43 
    # images a list of all images 
    # each image is a numpy ndarray with dimensions MG_WIDTH x IMG_HEIGHT x 3
    # labels a list of integer should be 0 we will append it 
    # this shit is what i give the function
    # data dir =C:\Users\HAREL\Desktop\AI\project5\traffic\gtsrb
    data_labels = []
    data_ndarray  = []
    for foldername in os.listdir(data_dir):
        print(foldername)
        for filename in os.listdir(os.path.join(data_dir,foldername)):
            filepath = (os.path.join(data_dir,foldername,filename))
            imagenumpy = cv2.imread(filepath)
            resized_image = cv2.resize(imagenumpy, (IMG_WIDTH, IMG_HEIGHT))
            data_labels.append(int(foldername))
            data_ndarray.append(resized_image)
            # resided image this is the input

         # print(os.path.join(directory, filename))
    return (data_ndarray,data_labels)

    


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([

    # Convolutional layer. Learn 32 filters using a 3x3 kernel 64 is 2times slower 
    tf.keras.layers.Conv2D(
        32, (3, 3), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
    ),

    # Max-pooling layer, 2*2 is slower by 15 seconds but better at 9 %
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),


    # Flatten units
    tf.keras.layers.Flatten(),

    # Add a hidden layer with dropout 0.3 is better than 0.2 elu is better then relu 
    # 500 *2 is better than 300*2 
    # and 1000
    # drop out is adding time 
    tf.keras.layers.Dense(500, activation="elu"),
    tf.keras.layers.Dense(500, activation="elu"),
    tf.keras.layers.Dropout(0.3),

    # add out put layer for all num catagories 
    tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
])

# Train neural network
    model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

    return model


if __name__ == "__main__":
    main()
