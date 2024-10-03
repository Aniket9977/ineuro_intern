import speech_recognition as sr
import logging

# Speech to Text Conversion Function
def convert_audio_to_text(audio_file_path):
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()

        # Load audio file
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)

        # Recognize (convert audio to text)
        text = recognizer.recognize_google(audio_data)
        logging.info("Audio successfully converted to text")
        return text

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return str(e)
