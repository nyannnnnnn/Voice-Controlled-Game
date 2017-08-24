# -*- coding: utf-8 -*-
import random
import cocos
from pill import Pill

class upTube(cocos.sprite.Sprite):
    def __init__(self, game):
        super(upTube, self).__init__('black.png')
        self.game = game
        self.ppx = game.ppx
        self.floor = game.floor
        self.active = True
        self.image_anchor = 0, 0
        self.num = 0
        self.opacity = 120
        self.reset()
        self.schedule(self.update)

    def update(self, dt):
        if self.active and self.x < self.ppx.x :
            self.active = False
            self.game.add_score()
        if self.x + self.width + self.game.floor.x < -10:
            self.reset()

    def reset(self):
        pitch = [16, 8, 4, 2, 1]
        x, y = self.game.last_block
        self.num = pitch[random.randrange(0, 4)]
        if x == 0:
            self.scale_x = 5
            self.scale_y = 1
            self.position = 0, 400
            self.active = False
        else:
            self.scale_x = 0.3 + random.random()
            #self.scale_y = min(max(y - 50 + random.random() * 100, 50), 300) / 100.0
            self.scale_y = -1 - random.random()
            self.position = x + 80 + (10 / pitch[random.randint(0, 4)]) * 10, 480#random.randint(480, 600)
            self.active = True
            # random add pill
            #if self.x > 1000 and random.random() > 0.6:
                #self.floor.add(Pill(self))
        self.game.last_block = self.x + self.width, self.height
