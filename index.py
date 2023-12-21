import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
import sys

# настройки
opts = {
    "alias": ('джарвис'),#, '', '', '', '', '', '', '', ''),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),#, '', '', '', '', '', '', ''),
    "cmds": {
        "ctime": ('текущее время','сейчас времени','который час'),#, '', '', '', '', '', '', ''),
        "exit": ('пока','сейчас времени','который час')#, '', '', '', '', '', '', ''),
    }
}

# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Джарвису
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])


    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC

def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    if cmd == 'exit':
        speak("До скорого сер")
        sys.exit()
    else:
        print('Команда не распознана, повторите!')

speak_engine = pyttsx3.init()

speak("Приветствую вас ")
speak("")

#Запуск программы
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)	# active microphone index

while True:
  with m as source:
    audio = r.listen(source)
  callback(r, audio)