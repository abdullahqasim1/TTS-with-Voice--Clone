import pyttsx3

def save_speech(text, speed, voice, filename):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.setProperty('voice', voice)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    engine.stop()

def get_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.stop()
    return voices

def speak(text, speed, voice):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.setProperty('voice', voice)
    engine.say(text)
    engine.runAndWait()
    engine.stop()

