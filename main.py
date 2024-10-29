
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.loader import Loader
from kivy.uix.image import Image, AsyncImage
from kivy.network.urlrequest import UrlRequest
from kivy.core.audio import SoundLoader
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.video import Video
#from kivy.clock import Clock
from plyer import notification
import webbrowser
from kivy.core.window import Window
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.utils import platform
import os
import sys
from plyer import tts
import plyer
#import pygame
# from pdf2image import convert_from_path

if platform == "android":
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.CAMERA,Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE])

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient kivy_gradient.Gradient

<Box@MDBoxLayout>:
    #md_bg_color:app.theme_cls.primary_dark
    spacing:"3dp"
    padding:'2dp'


<Crd@MDCard>:


<Lyt@MDRelativeLayout>:


<Btn1@MDRaisedButton>:


<IBtn2@MDIconButton>:

<Txt1@MDTextField>:

<Lbl@MDLabel>:
Screen:
    Box:
        id:bo
        orientation:'vertical'
        canvas.before:
            Rectangle:
                size: self.size
                pos: self.pos
                texture:
                    Gradient.vertical(
                    get_color_from_hex("#6063d8"),
                    get_color_from_hex("#c671e6"),
                    get_color_from_hex("#2A3699"),

                    )
        Lyt:
            id:ly

            Carousel:
                id:core
                size_hint:.9,.3
                pos_hint: {'center_x': 0.5,'center_y': 0.8}
                direction: 'right'
                anim_move_duration:0.8
                radius:[dp(25), dp(25), dp(25), dp(25)]
                Crd:
                    pos_hint: {'center_x': 0.5,'center_y': 0.5}
                    id:video_play_crd


                Crd:
                    pos_hint: {'center_x': 0.5,'center_y': 0.5}
                    id:u_video_play_crd
                   
              

                AsyncImage:
                    source: 'https://cdn.pixabay.com/animation/2022/07/29/03/42/03-42-11-849_256.gif'



            MDIconButton:
                icon:"api"
                pos_hint: {'center_x': 0.12,'center_y': 0.55}
                md_bg_color:"white"
                on_press:app.url_req()
            MDIconButton:
                icon:"file-pdf-box"
                md_bg_color:"white"
                pos_hint: {'center_x': 0.3,'center_y': 0.55}
                on_press:app.pdf_to_image_covert1()
            MDIconButton:
                icon: "speaker-message"
                md_bg_color:"red"
                pos_hint: {'center_x': 0.5,'center_y': 0.55}
                on_press:app.text_to_speach()
                icon_size: "25sp"
                theme_icon_color: "Custom"
                icon_color: app.theme_cls.primary_color
            MDIconButton:
                icon:"play"
                md_bg_color:"white"
                pos_hint: {'center_x': 0.7,'center_y': 0.55}
                on_press:app.video_play()
            MDIconButton:
                icon:"volume-high"
                md_bg_color:"white"
                pos_hint: {'center_x': 0.9,'center_y': 0.55}
                on_press:app.sound_play()


            Box:
                size_hint:1,.5
                md_bg_color:"blue"
                radius:[dp(25), dp(25), dp(0), dp(0)]
                # ScrollView:
                #     do_scroll_x: False
                #     do_scroll_y: True
                #     size_hint_y:.7
                #     size_hint_x:.96
                #     pos_hint:{'x':.05,'y':.05}
                #     MDGridLayout:
                #         cols:1
                #         size:(root.width,root.height)
                #         height:self.minimum_height
                #         #row_default_height:500
                #         #row_force_default: True
                #         Crd:
                #             size_hint:.5,.1

            MDRaisedButton:
                pos_hint: {'center_x': 0.5,'center_y': 0.4}
                on_press:app.open_file_mgr()
                text:"FILE OPEN"
                size_hint:.5,.07

            MDRaisedButton:
                pos_hint: {'center_x': 0.5,'center_y': 0.25}
                on_press:app.back_ground()
                text:"back round process"
                size_hint:.5,.07
            MDRaisedButton:
                pos_hint: {'center_x': 0.5,'center_y': 0.1}
                on_press:app.web_open()
                text:"api payment link"
                size_hint:.5,.07


'''


class MainHwch(MDApp):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager =MDFileManager(
              select_path=self.filepath,
              exit_manager=self.exitmanger,
              preview=True
          )

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_string(KV)
    def on_start(self,**kwargs):
        if platform == "android":
          from android.permissions import request_permissions, Permission
          request_permissions([Permission.CAMERA,Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

    def url_req(self):
        try:
           self.req = UrlRequest('http://192.168.43.73/api',on_error=self.error_fun,on_success=self.scuess_full)
           self.req.wait()
        except:
            notification.notify(title='RequestService', message="error expect")
    def scuess_full(self, *args):
        d=self.req.result
        self.da=d['data']
        notification.notify(title='notification', message=self.da)
    def error_fun(self, *args):
        notification.notify(title='RequestService', message="error reponse")

    def web_open(self):
        webbrowser.open('http://192.168.43.73:5000/payment_link')

    def filepath(self,path):
        self.dir=path
        self.exitmanger()
        toast(path)
    def open_file_mgr(self):
        if platform == "android":
            self.file_manager.show(f'{os.environ["EXTERNAL_STORAGE"]}/')
            self.manager_open = True
        else:
            self.file_manager.show('/')
            self.manager_open = True
    def exitmanger(self,*args):
        self.manager_open = False
        self.file_manager.close()
    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''
        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def sound_play(self):
        sound = SoundLoader.load(self.dir+'/audio_test.wav')
        if sound:
            sound.play()

    def video_play(self):
        #v=VideoPlayer(source='vi.mp4',  state='play', options={'allow_stretch': True})
        video = Video(source=self.dir+'/vedio_test.mp4')
        video.state = "play"
        video.options = {'eos': 'loop'}
        video.allow_stretch = True
        video.loaded = True
        self.root.ids.video_play_crd.add_widget(video)

    def u_video_play(self):
        v=VideoPlayer(source='https://www.youtube.com/shorts/_YNmGquCZSE',  state='play', options={'allow_stretch': True})
        self.root.ids.u_video_play_crd.add_widget(v)

    def pdf_to_image_covert1(self):
        from pdf2jpg import pdf2jpg
        Source =self.dir+"/test.pdf"
        Destination = self.dir
        pdf2jpg.convert_pdf2jpg(Source,Destination)

    def back_ground(self, *args):
        if platform == 'android':
            from jnius import autoclass
            service = autoclass('org.test.pssapp5.ServiceMyservice')
            mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
            argument = ''
            service.start(mActivity, argument)
     
        plyer.notification.notify(title='RequestService', message="back ground funtion_TIME")

    def text_to_speach(self, *args):
      
        message = "Kivy is a great tool for developing Android Apps.jagan sir i speak jagan sir"
        tts.speak(message=message)


MainHwch().run()

