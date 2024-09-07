import speech_recognition as sr
import threading

stop_event = threading.Event()  # Global stop event

def recognize_speech_buffered():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    buffer = []

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Press stop to flush the buffer.")

        try:
            while not stop_event.is_set():  # Continue until stop_event is triggered
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)

                # Check if stop_event was triggered after listening
                if stop_event.is_set():
                    print("Stop event triggered, exiting recognition loop.")
                    break

                # Attempt to recognize the audio
                try:
                    text = recognizer.recognize_google(audio)
                    buffer.append(text)
                    print(f"Buffered text: {text}")
                except sr.UnknownValueError:
                    print("Could not understand audio, continuing...")

        except Exception as e:
            print(f"Error in recognition loop: {e}")
        
    print("Exiting loop and returning buffered text.")
    return " ".join(buffer)
