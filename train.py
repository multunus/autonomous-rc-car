#!/usr/bin/env python
"""Train ANN"""
import sys
import glob
import datetime
import time
import pickle
from numpy import array, zeros, r_
from numpy.random import seed, randn
from cost_function import cost_function, gradients
from scipy.optimize import fmin_l_bfgs_b
from scipy.misc import imread, imresize
from configuration import CLASSIFICATION_LABELS_AND_VALUES, IMAGE_DIMENSIONS
from configuration import LAMBDA, HIDDEN_LAYER_SIZE, CLASSIFICATION_LABELS

def load_images_to_array(classification_label_and_values):
    """Loads images to array"""
    training_image_array = array([zeros(IMAGE_DIMENSIONS[0] * IMAGE_DIMENSIONS[1])])
    training_image_value = array([[0, 0, 0, 0, 0]])
    print("Loading images to array...")
    for class_label, class_value in classification_label_and_values.iteritems():
        for filename in glob.glob("./"+class_label+"/*"):
            image_array = imread(filename, flatten=True)
            resized_image_array = imresize(image_array, IMAGE_DIMENSIONS)
            training_image_array = r_[training_image_array, [resized_image_array.flatten()]]
            training_image_value = r_[training_image_value, [class_value]]
    return (training_image_array, training_image_value)

def cost_function_wrapper(theta, cost_function_parameters):
    """Wrapper for the Cost Function"""
    cost_function_parameters['theta'] = theta
    return cost_function(cost_function_parameters)

def gradients_wrapper(theta, gradient_parameters):
    """Wrapper for Gradients"""
    gradient_parameters['theta'] = theta
    return gradients(gradient_parameters)

def prepare_function_parameters(input_parameters, training_parameters):
    """Prepare function parameters using input and training parameters"""
    function_parameters = {}
    function_parameters = input_parameters.copy()
    function_parameters.update(training_parameters)
    return function_parameters

def prepare_input_parameters(input_layer_size, hidden_layer_size, number_of_labels,
                             lambda_value):
    """Prepare input parameters as a dictionary"""
    input_parameters = {}
    input_parameters['input_layer_size'] = input_layer_size
    input_parameters['hidden_layer_size'] = hidden_layer_size
    input_parameters['number_of_labels'] = number_of_labels
    input_parameters['lambda_value'] = lambda_value
    return input_parameters

def prepare_training_parameters(x_values, y_values):
    """Prepare training parameters"""
    training_parameters = {}
    training_parameters['x_values'] = x_values
    training_parameters['y_values'] = y_values
    return training_parameters

def initialize_theta(input_layer_size, hidden_layer_size, number_of_labels):
    """Initialize theta with samples from a standard normal distribution"""
    seed(0)
    return randn(((input_layer_size + 1) * hidden_layer_size) +
                 ((hidden_layer_size + 1) * number_of_labels))

def minimize_cost_function(initial_theta, function_parameters):
    """Minimize the Cost Function"""
    return fmin_l_bfgs_b(cost_function_wrapper, initial_theta,
                         fprime=gradients_wrapper, args=[function_parameters])

def save_model(hidden_layer_size, optimized_theta, lambda_value):
    """Save the model"""
    model = {'hidden_layer_size': hidden_layer_size, 'optimized_theta': optimized_theta,
             'lambda_value': lambda_value}
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    lambda_value_and_hidden_layers = "_l" + str(lambda_value) + "_h" + str(hidden_layer_size)
    timestamp_with_lambda_value = timestamp + lambda_value_and_hidden_layers
    model_filename = "model_" + timestamp_with_lambda_value + ".pkl"
    with open("optimized_thetas/" + model_filename, 'wb') as output_file:
        pickle.dump(model, output_file, pickle.HIGHEST_PROTOCOL)

def main():
    """Main function"""
    lambda_value = LAMBDA
    hidden_layer_size = HIDDEN_LAYER_SIZE
    try:
        lambda_value = float(sys.argv[1])
        hidden_layer_size = int(sys.argv[2])
    except(NameError, IndexError):
        print("Unspecified Lambda value and hidden layer size")
    image_array, image_values = load_images_to_array(CLASSIFICATION_LABELS_AND_VALUES)
    number_of_labels = len(CLASSIFICATION_LABELS)
    x_values = image_array[1:, :]
    y_values = image_values[1:, :]
    input_layer_size = x_values.shape[1]
    initial_theta = initialize_theta(input_layer_size, hidden_layer_size,
                                     number_of_labels)
    input_parameters = prepare_input_parameters(input_layer_size,
                                                hidden_layer_size,
                                                number_of_labels,
                                                lambda_value)
    training_parameters = prepare_training_parameters(x_values, y_values)
    function_parameters = prepare_function_parameters(input_parameters,
                                                      training_parameters)
    (optimized_theta, function_min_value, info_dict) = minimize_cost_function(initial_theta,
                                                                              function_parameters)
    print(function_min_value)
    print(info_dict)
    save_model(hidden_layer_size, optimized_theta, lambda_value)


if __name__ == '__main__':
    main()
