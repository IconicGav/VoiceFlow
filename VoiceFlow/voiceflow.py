import threading
from listener import start_listener
from speech_to_text import recognize_speech_buffered as recognize_speech
from typer import type_text

def main():
    print("VoiceFlow is starting...")

    listener_thread = threading.Thread(
        target=start_listener, args=(recognize_speech, type_text), daemon=True
    )
    listener_thread.start()

    try:
        while listener_thread.is_alive():
            listener_thread.join(1)  # Check for interruptions every 1 second
    except KeyboardInterrupt:
        print("\nVoiceFlow terminated by user")

if __name__ == "__main__":
    main()
