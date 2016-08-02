#!/usr/bin/env python
"""Interactive control for the car"""
import time
import io
import pygame
import pygame.font
import picamera
import configuration
import helpers.motor_driver as motor_driver_helper
import helpers.image as image_helper

UP = LEFT = DOWN = RIGHT = ACCELERATE = DECELERATE = False

def get_keys():
    """Returns a tuple of (UP, DOWN, LEFT, RIGHT, change, ACCELERATE,
    DECELERATE, stop) representing which keys are UP or DOWN and
    whether or not the key states changed.
    """
    change = False
    stop = False
    key_to_global_name = {
        pygame.K_LEFT: 'LEFT',
        pygame.K_RIGHT: 'RIGHT',
        pygame.K_UP: 'UP',
        pygame.K_DOWN: 'DOWN',
        pygame.K_ESCAPE: 'QUIT',
        pygame.K_q: 'QUIT',
        pygame.K_w: 'ACCELERATE',
        pygame.K_s: 'DECELERATE'
    }
    for event in pygame.event.get():
        if event.type in {pygame.K_q, pygame.K_ESCAPE}:
            stop = True
        elif event.type in {pygame.KEYDOWN, pygame.KEYUP}:
            down = (event.type == pygame.KEYDOWN)
            change = (event.key in key_to_global_name)
            if event.key in key_to_global_name:
                globals()[key_to_global_name[event.key]] = down
    return (UP, DOWN, LEFT, RIGHT, change, ACCELERATE, DECELERATE, stop)


def interactive_control():
    """Runs the interactive control"""
    setup_interactive_control()
    clock = pygame.time.Clock()
    with picamera.PiCamera() as camera:
        camera.resolution = configuration.PICAMERA_RESOLUTION
        camera.framerate = configuration.PICAMERA_FRAMERATE
        time.sleep(configuration.PICAMERA_WARM_UP_TIME)
        # GPIO.output(BACK_MOTOR_ENABLE_PIN, True)
        pwm = motor_driver_helper.get_pwm_imstance()
        motor_driver_helper.start_pwm(pwm)
        command = 'idle'
        duty_cycle = configuration.INITIAL_PWM_DUTY_CYCLE
        while True:
            up_key, down, left, right, change, accelerate, decelerate, stop = get_keys()
            if stop:
                break
            if accelerate:
                duty_cycle = duty_cycle + 3 if (duty_cycle + 3) <= 100 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                print("speed: " + str(duty_cycle))
            if decelerate:
                duty_cycle = duty_cycle - 3 if (duty_cycle - 3) >= 0 else duty_cycle
                motor_driver_helper.change_pwm_duty_cycle(pwm, duty_cycle)
                print("speed: " + str(duty_cycle))
            if change:
                command = 'idle'
                motor_driver_helper.set_idle_mode()
                if up_key:
                    command = 'forward'
                    print(duty_cycle)
                    motor_driver_helper.set_forward_mode()
                elif down:
                    command = 'reverse'
                    motor_driver_helper.set_reverse_mode()

                append = lambda x: command + '_' + x if command != 'idle' else x

                if left:
                    command = append('left')
                    motor_driver_helper.set_left_mode()
                elif right:
                    command = append('right')
                    motor_driver_helper.set_right_mode()
            print(command)
            stream = io.BytesIO()
            camera.capture(stream, format='jpeg', use_video_port=True)
            image_helper.save_image_with_direction(stream, command)
            stream.flush()

            clock.tick(30)
        pygame.quit()

def setup_interactive_control():
    """Setup the Pygame Interactive Control Screen"""
    pygame.init()
    display_size = (300, 400)
    screen = pygame.display.set_mode(display_size)
    background = pygame.Surface(screen.get_size())
    color_white = (255, 255, 255)
    display_font = pygame.font.Font(None, 40)
    pygame.display.set_caption('RC Car Interactive Control')
    text = display_font.render('Use arrows to move', 1, color_white)
    text_position = text.get_rect(centerx=display_size[0] / 2)
    background.blit(text, text_position)
    screen.blit(background, (0, 0))
    pygame.display.flip()

def main():
    """Main function"""
    motor_driver_helper.set_gpio_pins()
    interactive_control()

if __name__ == '__main__':
    main()
