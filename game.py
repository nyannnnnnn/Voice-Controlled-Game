#coding: utf8
import cocos
from cocos.sprite import Sprite
from pyaudio import PyAudio, paInt16
from cocos.audio import pygame
from cocos.actions import *
import struct
from ppx import PPX
from block import Block
from flappy import Flappy
from gameover import Gameover
from defines import *
from tube import Tube
from Uptube import upTube
from cocos.scenes import *
class VoiceGame(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame, self).__init__(255, 255, 255, 255, WIDTH, HEIGHT)
        pygame.mixer.init()
        self.cloud = cocos.sprite.Sprite('back.PNG')
        self.cloud.scale_x= 0.38
        self.cloud.scale_y = 0.45
        self.cloud.position = 300, 240
        self.add(self.cloud)
        self.gameover = None

        self.score = 0  # record score
        self.txt_score = cocos.text.Label(u'Score：0',
                                          font_name=FONTS,
                                          font_size=16,
                                          color=BLACK)
        self.txt_score.position = 500, 440
        self.add(self.txt_score, 99999)

        self.top = '', 0
        self.top_notice = cocos.text.Label(u'',
                                          font_name=FONTS,
                                          font_size=18,
                                          color=BLACK)
        self.top_notice.position = 400, 410
        self.add(self.top_notice, 99999)

        self.name = ''

        # init voice
        self.NUM_SAMPLES = 2048  # the size of memeory
        self.LEVEL = 1500  # save the sound selve

        self.voicebar = Sprite('black.png', color=(0, 0, 255))
        self.voicebar.position = 20, 450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)

        self.ppx = PPX(self)
        self.add(self.ppx)

        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        self.last_block = 0, 100
        for i in range(5):
            b = Block(self)
            self.floor.add(b)
            self.pitch_pic(b)
            pos = b.x + b.width, b.height

        # input the voice
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.stream.stop_stream()

        pygame.music.load('intro.wav'.encode())
        pygame.music.play(1)

        self.schedule(self.update)
    def pitch_pic(self, b):
        if b.num == 16:
            sprite = cocos.sprite.Sprite('sixteenth_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y
            self.floor.add(sprite)
        elif b.num == 8:
            sprite = cocos.sprite.Sprite('eighth_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y

            self.floor.add(sprite)
        elif b.num == 4:
            sprite = cocos.sprite.Sprite('quarter_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y

            self.floor.add(sprite)
        elif b.num == 2:
            sprite = cocos.sprite.Sprite('half_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y

            self.floor.add(sprite)
        elif b.num == 1:
            sprite = cocos.sprite.Sprite('whole_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y
            self.floor.add(sprite)
    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def collide(self):
        px = self.ppx.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.ppx.width * 0.8 and px + self.ppx.width * 0.2 <= b.x + b.width:
                if self.ppx.y < b.height + b.y:
                    self.ppx.land(b.height + b.y)
                    break

    def update(self, dt):
        # input num_smaples
        if self.stream.is_stopped():
            self.stream.start_stream()
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('2048h', string_audio_data))
        # print k
        self.voicebar.scale_x = k / 10000.0
        if k > 3000:
            if not self.ppx.dead:
                self.floor.x -= min((k / 20.0), 150) * dt
        if k > 8000:
            self.ppx.jump((k - 8000) / 25.0)
        self.floor.x -= self.ppx.velocity * dt
        self.collide()
        self.top_notice.x -= 80 * dt
        if self.top_notice.x < -700:
            self.top_notice.x = 700

    def reset(self):
        self.floor.x = 0
        self.last_block = 0, 100
        for b in self.floor.get_children():
            if isinstance(b, Block):
                b.reset()
            else:
                self.floor.remove(b)
        for b in self.floor.get_children():
            if isinstance(b, Block):
                self.pitch_pic(b)
        self.score = 0
        self.txt_score.element.text = u'Score：0'
        self.ppx.reset()
        if self.gameover:
            self.remove(self.gameover)
            self.gameover = None
        self.stream.start_stream()
        self.resume_scheduler()
        pygame.music.play(1)

        #self.pause_scheduler()
        #self.restart()
    def restart(self):
        cocos.director.director.replace(FadeTRTransition(first_scene, duration=2))
    def end_game(self):
        self.stream.stop_stream()
        self.pause_scheduler()
        # self.unschedule(self.update)
        self.gameover = Gameover(self)
        self.add(self.gameover, 100000)

    def show_top(self):
        self.remove(self.gameover)
        self.gameover = None
    def add_score(self):
        self.score += 10
        self.txt_score.element.text = u'Score：%d' % self.score

# start page
class Hello(cocos.layer.ColorLayer):
     is_event_handler = True
     def __init__(self):
          super(Hello, self).__init__(128, 222, 234, 255)
          menu = cocos.menu.Menu(u'Mode')
          menu.font_title['font_name'] = FONTS
          menu.font_item['font_name'] = FONTS
          menu.font_item['color'] = PINK
          menu.font_item_selected['font_name'] = PERPOR
          menu.font_item_selected['color'] = PERPOR
          mario_game = cocos.menu.MenuItem(u'Mario', self.mario)
          mario_game.y = 20
          #menu.create_menu([mario_game])
          bird_game = cocos.menu.MenuItem(u'Flappy Bird', self.bird)
          bird_game.y = -10
          menu.create_menu([mario_game, bird_game])
          self.add(menu)
     def bird(self):
          cocos.director.director.replace(second_scence)
     def mario(self):
          cocos.director.director.replace(FadeTRTransition(main_scene, duration=2))

class VoiceGame2(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame2, self).__init__(255, 255, 255, 255, WIDTH, HEIGHT)
        pygame.mixer.init()
        self.cloud = cocos.sprite.Sprite('fla.png')
        self.cloud.scale_x= 1.5
        self.cloud.scale_y = 1.83
        self.cloud.position = 300, 240
        self.add(self.cloud)
        self.gameover = None
        self.score = 0  #count score
        self.txt_score = cocos.text.Label(u'Score：0',
                                          font_name=FONTS,
                                          font_size=16,
                                          color=BLACK)
        self.txt_score.position = 510, 240
        self.add(self.txt_score, 99999)

        self.top = '', 0
        self.top_notice = cocos.text.Label(u'',
                                          font_name=FONTS,
                                          font_size=18,
                                          color=BLACK)
        self.top_notice.position = 400, 410
        self.add(self.top_notice, 99999)

        self.name = ''

        # init voice
        self.NUM_SAMPLES = 2048  # pyAudio cache size
        self.LEVEL = 1500  # sound threshold

        '''self.voicebar = Sprite('black.png', color=(0, 0, 255))
        self.voicebar.position = 20, 450
        self.voicebar.scale_y = 0.1
        self.voicebar.image_anchor = 0, 0
        self.add(self.voicebar)'''

        self.ppx = Flappy(self)
        self.add(self.ppx)
        self.floor2 = cocos.cocosnode.CocosNode()
        self.floor = cocos.cocosnode.CocosNode()
        self.add(self.floor)
        self.add(self.floor2)
        self.last_block = 0, 100
        for i in range(5):
            b = Tube(self)
            u = upTube(self)
            self.floor.add(b)
            self.floor.add(u)
            self.pitch_pic(u)
            pos = b.x + b.width, b.height

        # start inputing sound
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.stream.stop_stream()

        pygame.music.load('intro.wav'.encode())
        pygame.music.play(1)

        self.schedule(self.update)

    def on_mouse_press(self, x, y, buttons, modifiers):
        pass

    def collide(self):
        px = self.ppx.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.ppx.width * 0.8 and px + self.ppx.width * 0.2 <= b.x + b.width and isinstance(b, Tube):
                if self.ppx.y < b.height:
                    self.ppx.land(b.height)
                    break
            elif b.x <= px + self.ppx.width * 0.8 and px + self.ppx.width * 0.2 <= b.x + b.width and isinstance(b, upTube):
                if self.ppx.y + self.ppx.height > b.y + b.height:
                    self.ppx.land(b.y + b.height)
                    break
    def pitch_pic(self, b):
        if b.num == 16:
            sprite = cocos.sprite.Sprite('sixteenth_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y + b.height
            self.floor.add(sprite)
        elif b.num == 8:
            sprite = cocos.sprite.Sprite('eighth_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y + b.height

            self.floor.add(sprite)
        elif b.num == 4:
            sprite = cocos.sprite.Sprite('quarter_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y + b.height

            self.floor.add(sprite)
        elif b.num == 2:
            sprite = cocos.sprite.Sprite('half_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y + b.height

            self.floor.add(sprite)
        elif b.num == 1:
            sprite = cocos.sprite.Sprite('whole_note.png')
            sprite.scale = 0.1
            sprite.position = b.x - sprite.width,  b.y + b.height
            self.floor.add(sprite)

    def update(self, dt):
        # read NUM_SAMPLES of samples
        if self.stream.is_stopped():
            self.stream.start_stream()
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(struct.unpack('2048h', string_audio_data))
        # print k
        #self.voicebar.scale_x = k / 10000.0
        #if k > 3000:
        if not self.ppx.dead:
            self.floor.x -= min((3000 / 20.0), 150) * dt
        if k > 7000:
            self.ppx.jump((k - 8000) / 25.0)
        self.floor.x -= self.ppx.velocity * dt
        self.collide()
        self.top_notice.x -= 80 * dt
        if self.top_notice.x < -700:
            self.top_notice.x = 700

    def reset(self):
        self.floor.x = 0
        self.last_block = 0, 100
        for b in self.floor.get_children():
            if isinstance(b, Tube) or isinstance(b, upTube):
                b.reset()
            else:
                self.floor.remove(b)
        for b in self.floor.get_children():
            if isinstance(b, upTube):
                self.pitch_pic(b)
        self.score = 0
        self.txt_score.element.text = u'Score：0'
        self.ppx.reset()
        if self.gameover:
            self.remove(self.gameover)
            self.gameover = None
        self.stream.start_stream()
        self.resume_scheduler()
        pygame.music.play(1)

        #self.pause_scheduler()
        #self.restart()
    def restart(self):
        cocos.director.director.replace(FadeTRTransition(first_scene, duration=2))
    def end_game(self):
        self.stream.stop_stream()
        self.pause_scheduler()
        # self.unschedule(self.update)
        self.gameover = Gameover(self)
        self.add(self.gameover, 100000)

    def show_top(self):
        self.remove(self.gameover)
        self.gameover = None
    def add_score(self):
        self.score += 10
        self.txt_score.element.text = u'Score：%d' % self.score

cocos.director.director.init(caption="COMP4441")
voice_game = VoiceGame()
voice_game2 = VoiceGame2()
hello_layer = Hello()
first_scene = cocos.scene.Scene(hello_layer)
main_scene = cocos.scene.Scene(voice_game)
second_scence = cocos.scene.Scene(voice_game2)
cocos.director.director.run(first_scene)


