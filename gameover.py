# -*- coding: utf-8 -*-
import cocos
import urllib
#import urllib2
from defines import *

class Gameover(cocos.layer.ColorLayer):
    def __init__(self, game):
        super(Gameover, self).__init__(0, 150, 136, 240, WIDTH, HEIGHT)
        self.game = game
        self.billboard = None
        self.score = cocos.text.Label(u'Score：%d' % self.game.score,
                                      font_name=FONTS,
                                      font_size=36,
                                      color = (255, 255, 255, 255))
        self.score.position = 230, 300
        self.add(self.score)

        menu = cocos.menu.Menu(u'Game Over')
        menu.font_title['font_name'] = FONTS
        menu.font_item['color'] = PINK
        menu.font_item['font_name'] = PINK
        menu.font_item_selected['font_name'] = FONTS
        replay = cocos.menu.MenuItem(u'Play Again', self.replay)
        replay.y = 0
        replay.x = 0
        menu.create_menu([replay])
        self.add(menu)

    def replay(self):
        self.game.reset()
