#!/usr/bin/env python
"""Cost Function"""
import numpy
from sigmoid import sigmoid
from sigmoid_gradient import sigmoid_gradient

def cost_function(cost_function_parameters):
    """Cost function"""
    theta = cost_function_parameters['theta']
    input_layer_size = cost_function_parameters['input_layer_size']
    hidden_layer_size = cost_function_parameters['hidden_layer_size']
    num_labels = cost_function_parameters['number_of_labels']
    x_values = cost_function_parameters['x_values']
    y_values = cost_function_parameters['y_values']
    lambda_value = cost_function_parameters['lambda_value']

    theta_1_parameters = theta[0: (hidden_layer_size * (input_layer_size + 1))]
    theta_2_parameters = theta[(hidden_layer_size * (input_layer_size + 1)):]

    theta_1 = theta_1_parameters.reshape(hidden_layer_size, input_layer_size + 1)
    theta_2 = theta_2_parameters.reshape(num_labels, (hidden_layer_size + 1))

    input_examples_size = x_values.shape[0]

    hidden_layer_input = numpy.c_[numpy.ones(input_examples_size), x_values].dot(theta_1.T)
    hidden_layer_output = sigmoid(hidden_layer_input)

    output_layer_input = numpy.c_[numpy.ones(hidden_layer_output.shape[0]), hidden_layer_output].dot(theta_2.T)
    output = sigmoid(output_layer_input)

    first_part_of_cost = -((y_values) * numpy.log(output))
    second_part_of_cost = ((1.0 - y_values) * numpy.log(1.0-output))

    combined_thetas = numpy.append(theta_1.flatten()[1:], theta_2.flatten()[1:])
    regularization_term = (lambda_value/(2.0 * input_examples_size)) * numpy.sum(numpy.power(combined_thetas, 2))

    j = ((1.0/input_examples_size) * numpy.sum(numpy.sum(first_part_of_cost - second_part_of_cost))) + regularization_term
    return j


def gradients(gradient_parameters):
    """Gradient"""
    theta = gradient_parameters['theta']
    input_layer_size = gradient_parameters['input_layer_size']
    hidden_layer_size = gradient_parameters['hidden_layer_size']
    number_of_labels = gradient_parameters['number_of_labels']
    x_values = gradient_parameters['x_values']
    y_values = gradient_parameters['y_values']
    lambda_value = gradient_parameters['lambda_value']

    theta_1_params = theta[0: (hidden_layer_size * (input_layer_size + 1))]
    theta_2_params = theta[(hidden_layer_size * (input_layer_size + 1)):]

    theta_1 = theta_1_params.reshape(hidden_layer_size, input_layer_size + 1)
    theta_2 = theta_2_params.reshape(number_of_labels, (hidden_layer_size + 1))

    input_examples_size = x_values.shape[0]

    hidden_layer_input = numpy.c_[numpy.ones(input_examples_size), x_values].dot(theta_1.T)
    hidden_layer_output = sigmoid(hidden_layer_input)

    output_layer_input = numpy.c_[numpy.ones(hidden_layer_output.shape[0]), hidden_layer_output].dot(theta_2.T)
    output = sigmoid(output_layer_input)

    errors = output - y_values
    backpropagated_errors = errors.dot(theta_2[:, 1:]) * sigmoid_gradient(hidden_layer_input)

    delta_1 = backpropagated_errors.T.dot(numpy.c_[numpy.ones(input_examples_size), x_values])
    delta_2 = errors.T.dot(numpy.c_[numpy.ones(hidden_layer_output.shape[0]), hidden_layer_output])

    theta_1[:, 0] = 0
    theta_2[:, 0] = 0

    theta_1_gradient = ((1.0 / input_examples_size) * delta_1) + ((lambda_value / input_examples_size) * theta_1)
    theta_2_gradient = ((1.0 / input_examples_size) * delta_2) + ((lambda_value / input_examples_size) * theta_2)

    gradient = numpy.append(theta_1_gradient.flatten(), theta_2_gradient.flatten())
    return gradient
