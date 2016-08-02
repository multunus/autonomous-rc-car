#!/usr/bin/env python
"""Run the car autonomously"""
import time
import sys
import io
import picamera
import configuration
from predict import Predictor
import helpers.motor_driver as motor_driver_helper
import helpers.image as image_helper

def autonomous_control(model):
    """Run the car autonomously"""
    predictor = Predictor(model)
    with picamera.PiCamera() as camera:
        camera.resolution = configuration.PICAMERA_RESOLUTION
        camera.framerate = configuration.PICAMERA_FRAMERATE
        time.sleep(configuration.PICAMERA_WARM_UP_TIME)
        pwm = motor_driver_helper.get_pwm_imstance()
        motor_driver_helper.start_pwm(pwm)
        forward_cycle_count = left_cycle_count = right_cycle_count = 0
        should_brake = False

        while True:
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            direction = predictor.predict(stream)
            image_helper.save_image_with_direction(stream, direction)
            stream.flush()
            if direction == 'forward':
                should_brake = True
                left_cycle_count = right_cycle_count = 0
                forward_cycle_count = reduce_speed(pwm, forward_cycle_count)
                motor_driver_helper.set_front_motor_to_idle()
                motor_driver_helper.set_forward_mode()
            elif direction == 'left':
                should_brake = True
                forward_cycle_count = right_cycle_count = 0
                left_cycle_count = increase_speed_on_turn(pwm, left_cycle_count)
                motor_driver_helper.set_left_mode()
                motor_driver_helper.set_forward_mode()
            elif direction == 'right':
                should_brake = True
                forward_cycle_count = left_cycle_count = 0
                right_cycle_count = increase_speed_on_turn(pwm, right_cycle_count)
                motor_driver_helper.set_right_mode()
                motor_driver_helper.set_forward_mode()
            elif direction == 'reverse':
                should_brake = True
                motor_driver_helper.set_front_motor_to_idle()
                motor_driver_helper.set_reverse_mode()
            else:
                if should_brake:
                    print("braking...")
                    motor_driver_helper.set_reverse_mode()
                    time.sleep(0.2)
                    should_brake = False
                motor_driver_helper.set_idle_mode()
                forward_cycle_count = left_cycle_count = right_cycle_count = 0
                motor_driver_helper.change_pwm_duty_cycle(pwm, 100)
            print(direction)

def increase_speed_on_turn(pwm, turn_count):
    """Increase speed based on the turn count"""
    turn_count = turn_count + 1
    if turn_count > 4:
        print("Speed Increased")
        motor_driver_helper.change_pwm_duty_cycle(pwm, 100)
    else:
        motor_driver_helper.change_pwm_duty_cycle(pwm, 85)
    return turn_count

def reduce_speed(pwm, turn_count):
    """Reduce speed based on the turn count"""
    turn_count = turn_count + 1
    if turn_count < 3:
        motor_driver_helper.change_pwm_duty_cycle(pwm, 100)
    else:
        print("Speed reduced - Forward")
        motor_driver_helper.change_pwm_duty_cycle(pwm, 85)
    return turn_count

def main():
    """Main function"""
    model = None
    if len(sys.argv) > 1:
        model = sys.argv[1]
    motor_driver_helper.set_gpio_pins()
    autonomous_control(model)

if __name__ == '__main__':
    main()
