# -*- coding: utf-8 -*-
import cocos

class Pill(cocos.sprite.Sprite):
    def __init__(self, block):
        super(Pill, self).__init__('thirty_second_note.png')
        self.game = block.game
        self.ppx = block.game.ppx
        self.floor = block.floor
        self.block = block
        self.scale = 0.2
        self.position = block.x + block.width / 2, block.height + 100 + block.y

        self.schedule(self.update)

    def update(self, dt):
        px = self.ppx.x + self.ppx.width / 2 - self.floor.x
        py = self.ppx.y + self.ppx.height / 2 - self.floor.y

        if abs(px - self.x) < 50 and abs(py - self.y) < 50:
            # ppx get pill
            self.parent.remove(self)
            #self.ppx.rush()
            self.block.game.score += 20

    def reset(self):
        self.parent.remove(self)
