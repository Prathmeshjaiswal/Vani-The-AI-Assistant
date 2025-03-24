import speech_recognition as sr
import os

def say(text):
    os.system(f"say {text}")
    print("pycharm")
say("Hello my name is vani how may i help you plz tell me")
