# Python imports
import math

# Library imports
import sys
from enum import Enum

import pygame as pg

# pymunk imports
import pymunk as pm
from pymunk import Vec2d
import pymunk.pygame_util
WIDTH, HEIGHT = 1280, 720


class States(Enum):
    running = 1
    paused = 2
    menu = 3
    exit = 4


def spawn_ball(space, position):
    ball_body = pymunk.Body(1, float("inf"))
    ball_body.position = position

    ball_shape = pymunk.Circle(ball_body, 50)
    ball_shape.color = pg.Color("green")
    ball_shape.elasticity = 1.0

    # Keep ball velocity at a static value
    def constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * 400

    ball_body.velocity_func = constant_velocity

    space.add(ball_body, ball_shape)


class PhysicsSim:
    def __init__(self):
        pg.init()
        self._screen = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
        self._clock = pg.time.Clock()

        # Pygame stuff
        self._pasta_orig = pg.image.load('spaghetti.png')
        self._pasta = self._pasta_orig
        self._pasta_width, self._pasta_height = self._pasta.get_size()

        self._display = pg.Surface((int(WIDTH), int(HEIGHT)))

        # pymunk space
        self._space = pm.Space()
        self._space.gravity = (0, 0.0)
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Physics
        self._dt = 1.0 / 120.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 2

        self._debug = False

        # Execution control
        self._state = States.running

        spawn_ball(self._space, (WIDTH / 2, HEIGHT / 2))

    def run(self):
        """
        Game loop
        :return:
        """
        while True:
            # game running state
            if self._state == States.running:
                # Progress time forward
                self._process_time()
                self._process_events()
                self.update()
                self._clear_screen()
                self._draw()
                pg.display.flip()
                # Delay fixed time between frames
                self._clock.tick(60)
                pg.display.set_caption("fps: " + str(self._clock.get_fps()))

    def _process_time(self):
        """
        step forward in pymunk time
        :return:
        """
        for x in range(self._physics_steps_per_frame):
            self._space.step(self._dt)

    def _process_events(self):
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # game state event handler
            if self._state == States.running:
                if event.type == pg.KEYDOWN and event.key == pg.K_b:
                    self._debug = not self._debug
                # slow mo
                elif event.type == pg.KEYDOWN and event.key == pg.K_n:
                    if self._physics_steps_per_frame == 2:
                        self._physics_steps_per_frame = 1
                    else:
                        self._physics_steps_per_frame = 2
                # zoom in
                elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                    self.zoom_delta_x = -(self._pasta_height / self._pasta_width)
                    self.zoom_delta_y = -(self._pasta_width / self._pasta_height)
                elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                    self.zoom_delta_x = 2 * (self._pasta_height / self._pasta_width)
                    self.zoom_delta_y = 2 * (self._pasta_width / self._pasta_height)
                else:
                    self.zoom_delta_x, self.zoom_delta_y = (0, 0)

    def update(self):
        """
        Updates the states of all objects and the screen
        :return:
        """
        # self._car.update()
        # if self._level:
        #     self._level.update()
        w, h = self._pasta.get_size()
        if w >= 0 and h >= 0:
            self._pasta = pg.transform.scale(self._pasta_orig, (w + self.zoom_delta_x, h + self.zoom_delta_y))


    def _clear_screen(self):
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill((225, 225, 225))

    def _draw(self):
        """
        draws pygame objects/shapes
        :return:
        """
        # self._moving_background()
        if self._debug:
            self._space.debug_draw(self._draw_options)
        # self._display.fill((188, 55, 0))
        # self._display.blit(self._image, (0, 0))
        self._screen.blit(self._pasta, (0, 0))


if __name__ == "__main__":
    sim = PhysicsSim()
    sim.run()
