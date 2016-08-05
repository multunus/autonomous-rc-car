# autonomous-rc-car

This project aims to build an autonomous rc car using supervised learning of a neural network with a single hidden layer. We have not used any Machine Learning libraries since we wanted to implement the neural network from scratch to understand the concepts better. We have modified a remote controlled car to remove the dependency on the RF remote controller. A Raspberry Pi controls the DC motors via an L293D Motor Driver IC. You can find a post explaining this project in detail [here](http://www.multunus.com/blog/2016/07/autonomous-rc-car-using-raspberry-pi-and-neural-networks/). Here's a video of the car in action.

[![Autonomous RC car](https://img.youtube.com/vi/dCyBvLjW6X0/maxresdefault.jpg)](https://www.youtube.com/watch?v=dCyBvLjW6X0&vq=hd1080)

##Configuration

![Rc car controller circuit diagram](https://s3.amazonaws.com/multunus-images/rc_car_circuit_diagram.png)

We will be referring the DC motor controlling the left/right direction as the front motor and the motor controlling the forward/reverse direction as the back motor. Connect the ```BACK_MOTOR_DATA_ONE``` and ```BACK_MOTOR_DATA_TWO``` GPIO pins(`GPIO17` and `GPIO27`) of the Raspberry Pi to the Input pins for Motor 1(`Input 1`, `Input 2`) and the ```BACK_MOTOR_ENABLE_PIN``` GPIO pin(`GPIO22`) to the Enable pin for Motor 1(`Enable 1,2`) in the L293D Motor Driver IC. Connect the Output pins for Motor 1(`Output 1`, `Output 2`) of the IC to the back motor.

Connect the ```FRONT_MOTOR_DATA_ONE``` and ```FRONT_MOTOR_DATA_TWO``` GPIO pins(`GPIO19` and `GPIO26`) of the Raspberry Pi to the Input pins for Motor 2(`Input 3`, `Input 4`) in the IC. Connect the Output pins for Motor 2(`Output 3`, `Output 4`) of the IC to the front motor.

The ```PWM_FREQUENCY``` and ```INITIAL_PWM_DUTY_CYCLE``` represent the initial frequency and duty cycle of the PWM output.

We have created five class labels namely ```forward```, ```reverse```, ```left```, ```right``` and ```idle``` and assigned their expected values. All class labels would require a folder of the same name to be present in the current directory.

The input images resize to the dimension of the ```IMAGE_DIMENSION``` tuple value during training. The ```LAMBDA``` and ```HIDDEN_LAYER_SIZE``` values represent the default lambda value and the number of nodes in the hidden layer while training the neural network.

All these values are configurable in ```configuration.py```.

##Setup

The images for training are captured using ```interactive_control_train.py```, the car is controlled using the direction arrows and all the images are recorded in the same folder along with the corresponding key press. At the command prompt, run the following command:

```
python interactive_control_train.py
```

Data cleaning is done before segregating the images into their respective class folders based on the key press indicated in their filenames.

##Train

After segregating the images into their corresponding class folders, the neural network is trained using ```train.py``` which takes two optional arguments - ```lambda``` and ```hidden layer size```;  default values would be those specified in the configuration file. At the command prompt, run the following command:

```
python train.py 0.1 60
```

The images are loaded from the corresponding class folders and are assigned the class values indicated in the configuration file. The generated model is stored in the ```optimized_thetas``` folder as a pickle file.

##Run

Once we have the trained model, the RC car is run autonomously using ```autonomous.py``` which takes an optional argument for the trained model; default will use the latest model in the ```optimized_thetas``` folder. At the command prompt, run the following command:

```
python autonomous.py
```

We are reducing the speed of the car when the model predicts a turn. The reduction is not being made by the neural network, though we hope to add a speed component in the future.

##Planned features

We intend to add the following capabilities in the future:
* Control speed of the car using neural networks
* Stop signal detection
* Obstacle  detection

##Special Thanks

Thanks to [Andrew Ng](http://www.andrewng.org/) for his [Coursera course](http://www.coursera.org/learn/machine-learning) on Machine Learning.

##About

[![Multunus logo](https://camo.githubusercontent.com/c0701d8866d0962ddc36db56dbf1ce93d712800e/68747470733a2f2f73332e616d617a6f6e6177732e636f6d2f6d756c74756e75732d696d616765732f4d756c74756e75735f4c6f676f5f566563746f725f726573697a65642e706e67)](http://www.multunus.com/?utm_source=github)

autonomous-rc-car is maintained and funded by Multunus Software Pvt. Ltd.
The names and logos for Multunus are trademarks of Multunus Software Pvt. Ltd.

We built this to explore and learn Machine Learning concepts in our [20% investment time](http://www.multunus.com/blog/2016/01/20-investment-time-background-story/). We will be supporting this project during our investment time.
