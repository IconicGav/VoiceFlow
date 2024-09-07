# VoiceFlow
VoiceFlow – Highlights the seamless flow between speaking and typing.

How to Run the Project:
Activate the virtual environment (if not already activated):

bash
Copy code
venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the main script:

bash
Copy code
python VoiceFlow/voiceflow.py
Summary:
voiceflow.py: Entry point for the application.
listener.py: Listens for mouse clicks to trigger speech-to-text.
speech_to_text.py: Handles voice input and converts it to text.
typer.py: Types out the recognized text in the current active text field.
tests/: Directory for your unit tests.
