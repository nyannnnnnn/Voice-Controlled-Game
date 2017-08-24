# -*- coding: utf-8 -*-
import random
import cocos
from pill import Pill

class Block(cocos.sprite.Sprite):
    def __init__(self, game):
        super(Block, self).__init__('black.png')
        self.game = game
        self.ppx = game.ppx
        self.floor = game.floor
        self.active = True
        self.image_anchor = 0, 0
        #self.scale = 0.18
        self.num = 0
        self.opacity = 120
        self.reset()
        self.schedule(self.update)


    def update(self, dt):
        if self.active and self.x < self.ppx.x - self.floor.x:
            self.active = False
            self.game.add_score()
        if self.x + self.width + self.game.floor.x < -10:
            self.reset()
            self.game.pitch_pic(self)


    def reset(self):
        pitch = [16, 8, 4, 2, 1]
        x, y = self.game.last_block
        self.num = pitch[random.randint(0, 4)]
        if x == 0:
            self.scale_x = 5
            self.scale_y = 0.8
            self.position = 0, 0
            self.active = False
        else:
            y_position =  random.randrange(50, 150)
            self.scale_x = 0.75 + random.random() * 2
            #self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0
            self.scale_y = 0.5

            self.position = x + 60 + (10 / self.num) * 10,  y_position
            self.active = True
            # random add pill
            if self.x > 1000 and random.random() > 0.6:
                self.floor.add(Pill(self))
        self.game.last_block = self.x + self.width, self.height
