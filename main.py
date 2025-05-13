from kivymd.app import MDApp
from kivy.properties import StringProperty

import os
from os.path import dirname, join
import certifi

from kivy.core.window import Window

from uix.root import Root

from uix.baseclass.dirs import AppData
#from uix.baseclass.lang import Lang
#from uix.baseclass.android_perm import AndroidPermissions

#Set ssl file to reduce error on https requests
os.environ['SSL_CERT_FILE' ] = certifi.where()

locale_dir = join(dirname(__file__), 'uix', 'i18n')
#tr= Lang('en', locale_dir)
Window.size= (380, 680) #Remove before packaging

class MainApp(MDApp):
    title = "MenstrualHealth"
    icon='./assets/img/icon.png'
    locale_dir = join(dirname(__file__), 'uix', 'i18n')
    lang=StringProperty('en')
    main_color = (1, 0, 1, .8)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Setting the keyboard for the phone
        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.softinput_mode = "below_target"

        # Check for and set  theme of the app(Only dark and light)
        try:
            self.a_d= AppData.l_app_data()['theme']
            if self.a_d is not False: self.theme_cls.theme_style = self.a_d
        except:
            self.theme_cls.theme_style = 'Light'
            AppData._theme_add(theme='Light')

    def build(self):
        self.root = Root()
        #try:
        #    lang=self.n['lang']
        #    if lang == 'English': lang= 'en'
        #except:
        #    lang='en'
        #    Udata.stg_mother_lang_add(lang='English')
        #    Udata.stg_lang_foregn_add(lang='Swahili')
        #self.lang = lang
        self.root.set_current("initscreen")

    #def on_start(self):
    #    self.dont_gc = AndroidPermissions(self.start_app)

    #def start_app(self):
    #    self.dont_gc = None

    #def on_pause(self):
    #    return True

    #def on_lang(self, instance, lang):
    #    tr.switch_lang(lang, locale_dir)

MainApp().run()