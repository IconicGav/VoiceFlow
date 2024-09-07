from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key

def start_listener(on_start_speech, on_end_speech):
    is_recording = [False]

    def toggle_recording():
        if not is_recording[0]:
            is_recording[0] = True
            print("Start recording...")
            recognized_text = on_start_speech()
            if recognized_text:
                on_end_speech(recognized_text)
        else:
            is_recording[0] = False
            print("Stop recording.")

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
            return False  # Stop both listeners

    # Start mouse and keyboard listeners in parallel
    with MouseListener(on_click=on_click) as mouse_listener:
        with KeyboardListener(on_press=on_press) as keyboard_listener:
            mouse_listener.join()
            keyboard_listener.join()
