# -*- coding: utf-8 -*-
import cocos
import time
from pyglet import image
from cocos.audio import pygame

class Flappy(cocos.sprite.Sprite):
    def __init__(self, game):

        frame_1 = image.AnimationFrame(image.load('professor.png'), 0.15)
        frame_2 = image.AnimationFrame(image.load('professor2.png'), 0.15)
        self.frames = image.Animation([frame_1, frame_2])
        frame_rush_1 = image.AnimationFrame(image.load('ppx_rush1.png'), 0.15)
        frame_rush_2 = image.AnimationFrame(image.load('ppx_rush2.png'), 0.15)
        self.frames_rush = image.Animation([frame_rush_1, frame_rush_2])
        super(Flappy, self).__init__(self.frames)

        self.sound_rush = pygame.mixer.Sound("rush.wav")
        self.sound_die = pygame.mixer.Sound("die.wav")
        self.sound_jump = pygame.mixer.Sound("fly_sound.wav")
        self.sound_fall = pygame.mixer.Sound('fall_sound.wav')
        self.game = game
        self.dead = False
        self.can_jump = False
        self.speed = 0
        self.rush_time = 0
        self.velocity = 0
        self.image_anchor = 0, 0
        self.scale = 0.1
        self.position = 100, 300
        self.schedule(self.update)

    def jump(self, h):
        if self.dead:
            return
        #if self.can_jump:
        self.y += 1
        self.speed -= max(min(h, 350), 200)
        self.speed = max(-450, self.speed)
        #if self.can_jump:
        #self.sound_jump.play()
        self.can_jump = False
        


    def land(self, y):
        '''if self.dead:
            return
        if self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y = y'''
        self.die()

    def update(self, dt):
        if self.dead:
            return
        self.speed += 300 * dt
        self.y -= self.speed * dt * 0.4
        self.sound_fall.play()
        if self.rush_time > 0:
            self.rush_time -= dt
            if self.rush_time <= 0:
                self.velocity = 0
                self.image = self.frames
        if self.y < -150:
            self.die()

    def die(self):
        pygame.music.stop()
        self.sound_die.play()
        time.sleep(1.7)
        self.speed = 0
        self.dead = True
        self.game.end_game()

    def reset(self):
        self.can_jump = False
        self.dead = False
        self.speed = 0
        self.velocity = 0
        self.rush_time = 0
        self.position = 100, 300
        self.image = self.frames

    def rush(self):
        self.sound_rush.play()
        self.image = self.frames_rush
        self.velocity = 400
        self.rush_time = 3
        self.sound_rush.play()
