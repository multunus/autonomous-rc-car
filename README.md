# autonomous-rc-car

In this tutorial, we will be building an autonomous car using supervised learning of a neural network with a single hidden layer. We have modified a remote controlled car such that the dependency on the RF remote controller has been removed. The motors controlling the forward/reverse direction and the left/right direction are being controlled by a Raspberry Pi via a L293D Motor Driver IC.

##Configuration

The motor controlling the forward/reverse direction will be referred to as the back motor. The inputs to Motor 1 of the L293D Motor Driver IC are connected to the ```BACK_MOTOR_DATA_ONE``` and ```BACK_MOTOR_DATA_TWO``` GPIO pins of the Raspberry Pi. The enable pin for Motor 1 is connected to the ```BACK_MOTOR_ENABLE_PIN``` GPIO pin of the Raspberry Pi. The output pins for Motor 1 are connected to the back motor of the car.

The motor controlling the left/right direction will be referred to as the front motor. The inputs to Motor 2 of the L293D Motor Driver IC are connected to the ```FRONT_MOTOR_DATA_ONE``` and ```FRONT_MOTOR_DATA_TWO``` GPIO pins of the Raspberry Pi. The output pins for Motor 2 are connected to the front motor of the car.

The ```PWM_FREQUENCY``` and ```INITIAL_PWM_DUTY_CYCLE``` represent the initial frequency and duty cycle of the PWM output.

We have created five class labels namely ```forward```, ```reverse```, ```left```, ```right``` and ```idle``` and assigned the expected values for each class label. All class labels would require a folder of the same name to be present in the current directory.

The input images will be resized to the dimension of the ```IMAGE_DIMENSION``` tuple value. The ```LAMBDA``` and ```HIDDEN_LAYER_SIZE``` values represent the default lambda value and the number of nodes in the hidden layer while training the neural network.

All these values can be configured in ```configuration.py```.

##Setup

The images for training can be captured using ```interactive_control_train.py```, the car can be controlled using the direction arrows and all the images will be captured in the same folder along with the corresponding key press.

```
python interactive_control_train.py
```

Once enough images have been collected, it should be segregated into the corresponding class folders. This approach has been adopted to ensure that the data will be tidied up before it is input to the neural network.

##Train

After the images have been placed in their corresponding class folders, the neural network is trained using ```train.py``` which takes two optional arguments - ```lambda``` and ```hidden layer size```, the values set in the configuration file will be used by default. The images are loaded from the corresponding class folders and are assigned the class values indicated in the configuration file. The generated model is stored in the ```optimized_thetas``` folder as a pickle file.

```
python train.py 0.1 60
```

##Run

To run the car autonomously, use ```autonomous.py``` which takes an optional argument of the model to be used, the latest model file in the ```optimized_thetas``` folder by default.

```
python autonomous.py
```

##About

[![Multunus logo](https://camo.githubusercontent.com/c0701d8866d0962ddc36db56dbf1ce93d712800e/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6d756c74756e75732d696d616765732f4d756c74756e75735f4c6f676f5f566563746f725f726573697a65642e706e67)](http://www.multunus.com/)

autonomous-rc-car is maintained and funded by Multunus Software Pvt. Ltd.
The names and logos for Multunus are trademarks of Multunus Software Pvt. Ltd.

We built this to explore and learn Machine Learning concepts in our [20% investment time](http://www.multunus.com/blog/2016/01/20-investment-time-background-story/). We will be supporting this project during our investment time.
