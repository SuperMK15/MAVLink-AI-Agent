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
        audio = recognizer.listen(source, phrase_time_limit=15)

    try:
        text = recognizer.recognize_google(audio)
        if "write" in text.lower():
            text = text.lower().replace("write", "right")
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    
def listen_for_yes_no():
    """
    Listens for a yes or no response using the microphone and returns the recognized text.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.2 # Adjust this value as needed
    microphone = sr.Microphone()

    with microphone as source:
        print("Please say 'yes, I confirm' or 'no, cancel'")
        recognizer.adjust_for_ambient_noise(source)  # optional, reduces noise
        audio = recognizer.listen(source, phrase_time_limit=15)

    try:
        text = recognizer.recognize_google(audio)
        if "yes" in text.lower():
            return "yes"
        elif "no" in text.lower():
            return "no"
        else:
            return None
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
