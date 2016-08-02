#!/usr/bin/env python
"""Predict the direction based on image"""
import os
import glob
import operator
import pickle
from PIL import Image
from numpy import c_, asarray
from scipy.misc import imresize
from sigmoid import sigmoid
from configuration import CLASSIFICATION_LABELS, IMAGE_DIMENSIONS
from configuration import PICAMERA_RESOLUTION_WIDTH, PICAMERA_RESOLUTION_HEIGHT

class Predictor:
    """Predictor class for determining direction"""
    def __init__(self, model=None):
        model_file = ""
        if not model:
            model_file = max(glob.iglob('./optimized_thetas/*.pkl'), key=os.path.getctime)
        else:
            model_file = "./" + model
        print("\n\n\n" + model_file+"\n\n\n")
        self._open_model_file(model_file)

    def _open_model_file(self, model_file):
        with open(model_file, 'rb') as mod:
            self.model = pickle.load(mod)
        self.thetas = self.model['optimized_theta']
        self.hidden_layer_size = self.model['hidden_layer_size']

    def predict(self, stream):
        """Predicts the direction of movement based on the NN response"""
        input_layer_size, number_of_labels, x_value = _convert_stream_to_array(stream)
        theta1_params = self.thetas[0: (self.hidden_layer_size * (input_layer_size + 1))]
        theta2_params = self.thetas[(self.hidden_layer_size * (input_layer_size + 1)):]
        theta_1 = theta1_params.reshape(self.hidden_layer_size, input_layer_size + 1)
        theta_2 = theta2_params.reshape(number_of_labels, (self.hidden_layer_size + 1))
        first_layer_output = x_value.dot(theta_1.T)
        hidden_layer_input = sigmoid(first_layer_output)
        hidden_layer_output = c_[[1], [hidden_layer_input]].dot(theta_2.T)
        model_output = sigmoid(hidden_layer_output)

        index, value = max(enumerate(model_output[0]), key=operator.itemgetter(1))
        print(value)
        return CLASSIFICATION_LABELS[index]

    def change_model(self, model):
        """Change the current model of the predictor object"""
        model_file = "./"+ model
        self._open_model_file(model_file)


def _convert_stream_to_array(stream):
    stream.seek(0)
    image = Image.open(stream).convert('L')
    image = image.crop((0, PICAMERA_RESOLUTION_HEIGHT / 2, PICAMERA_RESOLUTION_WIDTH, PICAMERA_RESOLUTION_HEIGHT))
    image_array = asarray(image)
    resized_image_array = imresize(image_array, IMAGE_DIMENSIONS)
    input_layer_size = resized_image_array.flatten().shape[0]
    number_of_labels = len(CLASSIFICATION_LABELS)
    x_value = c_[[1], [resized_image_array.flatten()]].flatten()
    return (input_layer_size, number_of_labels, x_value)
