import kivy 
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window


from multiprocessing import Process
import keyboard
import pyttsx3
import sys


import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os

recognizer = sr.Recognizer()
mic = sr.Microphone()
translator = Translator()
engine = pyttsx3.init()

Builder.load_string("""
#:import utils kivy.utils

<MyLayout>
    GridLayout:
        cols: 1
        size: root.width, root.height
        
        Label:
            text: "MultiLanguage Assistant"
            color: (17/255,17/255,17/255,1)
            font_size: 32
            size_hint: 0.5, 0.7
        
        BoxLayout:
            size: root.width, root.height
            padding:50
            Label:
                text: "Select the Speaker Language"
                color: (17/255,17/255,17/255,1)
                font_size: 18
                size_hint: (None, None)
                width:250
                height: 50
            
            Spinner:
                id: spinner_ids
                text: "Language"
                values: ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
                size_hint: (None, None)
                on_text: root.spinnerIds(spinner_ids.text)
                #RGB - A
                background_normal: ''
                background_color:utils.get_color_from_hex('#72b2bb')
                width:200
                height: 50

        BoxLayout:
            size: root.width, root.height
            padding:50
            Label:
                text: "Select the Listener Language"
                color: (17/255,17/255,17/255,1)
                font_size: 18
                size_hint: (None, None)
                width:250
                height: 50
            
            Spinner:
                id: spinner_id
                text: "Language"
                values: ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
                size_hint: (None, None)
                on_text: root.spinnerIdl(spinner_id.text)
                #RGB - A
                background_normal: ''
                background_color:utils.get_color_from_hex('#72b2bb')
                width:200
                height: 50

        BoxLayout:
            size: root.width, root.height
            size_hint_y: 2
            padding:50
            Button: 
                text: "Tap to say something"
                #RGB - A
                background_normal: ''
                background_color:utils.get_color_from_hex('#72b2bb')
                size_hint: (None, None)
                width:200
                height: 50
                on_press: root.say_hello()
"""
)


class Translation:
    def __init__(self):
        self.lt_dict = {'Tamil' : 'ta', 'English':'en', 'Hindi':'hi', 'Japanese':'ja'}
        self.lr_dict = {'Tamil':'ta-IN', 'English':'en-IN', 'Hindi':'hi-IN', 'Japanese':'ja-JP'}
        self.audio_in_lt = 'en'
        self.audio_out_lt = 'en'
        self.audio_lang = 'en-IN'
        
    def detection(self, audio_in, audio_out, i):
        if i==1:
            with mic as source:
                print("Say 'Hello!'")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = recognizer.listen(source, phrase_time_limit=3)
                    Text = recognizer.recognize_google(audio)
                    Text = Text.lower()
                except sr.UnknownValueError:
                    print("Uh-ho! we didn't hear you... Try Again!")
                    self.detection()


            if 'hello' in Text:
                self.recognition(audio_in, audio_out)
                
        else:
            self.recognition(audio_in, audio_out)


    def recognition(self, audio_in, audio_out):
        self.audio_in_lt = self.lt_dict[audio_in]
        self.audio_out_lt = self.lt_dict[audio_out]
        self.audio_lang = self.lr_dict[audio_in]
        with mic as source:
            try:
                print("Say Something....")
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                
                audio = recognizer.listen(source, phrase_time_limit=5)
                
                statement = recognizer.recognize_google(audio, language = self.audio_lang)
                
                if 'stop' in statement:
                    sys.exit("Happy to help you..!")
                
                print("Phrase to be Translated : "+ statement)

                text_to_translate = translator.translate(statement, src= self.audio_in_lt, dest=self.audio_out_lt)
                
                text = text_to_translate.text
                speak = gTTS(text=text, lang=self.audio_out_lt, slow= False)
                
                filename = 'temp.mp3'
                speak.save(filename)
                playsound.playsound(filename)
                os.remove(filename)


            except sr.UnknownValueError:
                print("Unable to Understand the Input")
                
            except sr.RequestError as e:
                print("Unable to provide Required Output".format(e))



class MyLayout(Widget):
    def GridLayout(self):
        return
    def spinnerIds(self, value):
        global a_in
        print(f"Speaker Language {value}")
        a_in = value
    def spinnerIdl(self, value):
        global a_out
        print(f"Lintener Language {value}")
        a_out = value
    def say_hello(self):
        translator = Translation()
        i=1
        while True:
            if i%2!=0:
                translator.detection(a_in, a_out, i)
            else:
                translator.detection(a_out, a_in, i)
            i+=1    
    

class Communicator(App):
    def build(self):
        Window.clearcolor =(203/255.0,228/255.0,233/255.0, 1)
        return MyLayout()

if __name__=='__main__':
    Communicator().run()