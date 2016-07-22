#!/usr/bin/env python
"""Derivative of the Sigmoid Function"""
from sigmoid import sigmoid

def sigmoid_gradient(x_value):
    """Return value of derivative of Sigmoid function"""
    return sigmoid(x_value) * (1 - sigmoid(x_value))
