import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

audio_filepath="patient_voice_test_for_patient.mp3"
#record_audio(file_path=audio_filepath)

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
stt_model="whisper-large-v3"

# def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
#     client=Groq(api_key="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")
    
#     audio_file=open(audio_filepath, "rb")
#     transcription=client.audio.transcriptions.create(
#         model=stt_model,
#         file=audio_file,
#         language="en"
#     )

#     return transcription.text


from deep_translator import GoogleTranslator
from langdetect import detect  # install using: pip install langdetect

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file
        )

    original_text = transcription.text

    try:
        detected_lang = detect(original_text)
    except Exception as e:
        detected_lang = "en"  # fallback

    translated_text = GoogleTranslator(source=detected_lang, target="en").translate(original_text)

    return original_text, detected_lang, translated_text



