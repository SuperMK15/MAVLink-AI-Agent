import speech_recognition as sr
import pyttsx3

def listen_for_command():
    """
    Listens for a command using the microphone and returns the recognized text.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Please say something...")
        recognizer.adjust_for_ambient_noise(source)  # optional, reduces noise
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def say(text):
    """
    Uses text-to-speech to say the provided text.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
