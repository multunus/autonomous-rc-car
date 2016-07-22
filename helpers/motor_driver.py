"""Helpers for controlling the Front and Back Motors"""
import configuration
import RPi.GPIO as GPIO

BACK_MOTOR_DATA_ONE = configuration.BACK_MOTOR_DATA_ONE
BACK_MOTOR_DATA_TWO = configuration.BACK_MOTOR_DATA_TWO
BACK_MOTOR_ENABLE_PIN = configuration.BACK_MOTOR_ENABLE_PIN
FRONT_MOTOR_DATA_ONE = configuration.FRONT_MOTOR_DATA_ONE
FRONT_MOTOR_DATA_TWO = configuration.FRONT_MOTOR_DATA_TWO
PWM_FREQUENCY = configuration.PWM_FREQUENCY
INITIAL_PWM_DUTY_CYCLE = configuration.INITIAL_PWM_DUTY_CYCLE

def set_right_mode():
    """Set mode to Right"""
    GPIO.output(FRONT_MOTOR_DATA_ONE, True)
    GPIO.output(FRONT_MOTOR_DATA_TWO, False)

def set_left_mode():
    """Set mode to Left"""
    GPIO.output(FRONT_MOTOR_DATA_ONE, False)
    GPIO.output(FRONT_MOTOR_DATA_TWO, True)

def set_reverse_mode():
    """Set mode to Reverse"""
    GPIO.output(BACK_MOTOR_DATA_ONE, False)
    GPIO.output(BACK_MOTOR_DATA_TWO, True)

def set_forward_mode():
    """Set mode to Forward"""
    GPIO.output(BACK_MOTOR_DATA_ONE, True)
    GPIO.output(BACK_MOTOR_DATA_TWO, False)

def set_idle_mode():
    """Set mode to Idle"""
    set_back_motor_to_idle()
    set_front_motor_to_idle()

def set_back_motor_to_idle():
    """Sets the Back motor to Idle state"""
    GPIO.output(BACK_MOTOR_DATA_ONE, True)
    GPIO.output(BACK_MOTOR_DATA_TWO, True)

def set_front_motor_to_idle():
    """Sets the Front motor to Idle state"""
    GPIO.output(FRONT_MOTOR_DATA_ONE, True)
    GPIO.output(FRONT_MOTOR_DATA_TWO, True)

def set_gpio_pins():
    """Sets the GPIO pins for the two motors"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BACK_MOTOR_DATA_ONE, GPIO.OUT)
    GPIO.setup(BACK_MOTOR_DATA_TWO, GPIO.OUT)
    GPIO.setup(FRONT_MOTOR_DATA_ONE, GPIO.OUT)
    GPIO.setup(FRONT_MOTOR_DATA_TWO, GPIO.OUT)
    GPIO.setup(BACK_MOTOR_ENABLE_PIN, GPIO.OUT)

def get_pwm_imstance():
    """Returns a PWM instance"""
    return GPIO.PWM(BACK_MOTOR_ENABLE_PIN, PWM_FREQUENCY)

def start_pwm(pwm):
    """Starts the PWM with the initial duty cycle"""
    pwm.start(INITIAL_PWM_DUTY_CYCLE)

def change_pwm_duty_cycle(pwm, duty_cycle):
    """Change the PWM duty cycle"""
    pwm.ChangeDutyCycle(duty_cycle)
