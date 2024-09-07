from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key
import threading

stop_event = threading.Event()  # Global event to control when to stop recording
is_recording = False  # Simple boolean to track recording state
recognition_thread = None  # Variable to track the active recognition thread

def start_listener(on_start_speech, on_end_speech):
    global is_recording, recognition_thread
    speech_buffer = []  # Buffer for the text

    def toggle_recording():
        global is_recording, recognition_thread

        if not is_recording:
            is_recording = True
            stop_event.clear()  # Reset stop event
            speech_buffer.clear()  # Reset buffer for a new session
            print("Start recording...")

            # Start a new thread for speech recognition
            recognition_thread = threading.Thread(target=lambda: speech_buffer.append(on_start_speech()))
            recognition_thread.start()

        else:
            is_recording = False
            stop_event.set()  # Signal to stop recording
            print("Stop recording. Flushing buffer...")

            if recognition_thread:
                recognition_thread.join(timeout=5)  # Ensure the recognition thread stops

            final_text = " ".join(speech_buffer)  # Join all buffered speech
            print(f"Final text to type: {final_text}")  # Debugging the final text
            on_end_speech(final_text)  # Type out the complete text
            speech_buffer.clear()  # Clear buffer for the next session

    # Mouse event handler
    def on_click(x, y, button, pressed):
        if button == button.middle and pressed:
            toggle_recording()

    # Keyboard event handler
    def on_press(key):
        try:
            if key.char == '`':  # backtick key
                toggle_recording()
        except AttributeError:
            pass  # Handle special keys like Shift, Ctrl, etc.

        if key == Key.esc:
            print("Exit program triggered.")
            stop_event.set()  # Ensure the program exits on ESC
            if recognition_thread:
                recognition_thread.join(timeout=5)  # Ensure the recognition thread finishes before exiting
            return False  # Stop both listeners

    # Start mouse and keyboard listeners in parallel
    with MouseListener(on_click=on_click) as mouse_listener:
        with KeyboardListener(on_press=on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()
