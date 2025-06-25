# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="ನನ್ನ ಹೆಸರು ಅನೀಕೇತ್, ಮತ್ತು ನಾನು ರೈಮಯ್ಯ ಇನ್ಸ್ಟಿಟ್ಯೂಟ್ ಆಫ್ ಟೆಕ್ನಾಲಜಿಯಲ್ಲಿ ಓದುತ್ತಿದ್ದೇನೆ."
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")







from elevenlabs.client import ElevenLabs
from elevenlabs import save

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    # Initialize the client
    client = ElevenLabs(api_key="sk_57bc0ec633315fd9225f416d91570480326a25bb7e934623")

    # Get all voices and find 'Aria'
    voices = client.voices.get_all().voices
    voice = next((v for v in voices if v.name.lower() == "aria"), None)

    if voice is None:
        raise ValueError("Voice 'Aria' not found. Please check available voices.")

    # Generate audio using voice_id and model_id
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id=voice.voice_id,
        model_id="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )

    # Save audio
    save(audio, output_filepath)

# Run it
#text_to_speech_with_elevenlabs(input_text, "elevenlabs_testing.mp3")





#Step2: Use Model for Text output to Voice

from gtts import gTTS
from pydub import AudioSegment
import subprocess
import platform
import os

def text_to_speech_with_gtts(input_text, output_filepath_mp3):
    language = "en"

    # Generate MP3 using gTTS
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath_mp3)

    # Convert MP3 to WAV
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(output_filepath_mp3)
    sound.export(output_filepath_wav, format="wav")

    # Autoplay based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath_wav])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Usage
#text_to_speech_with_gtts("Hi, this is AI Doctor with Hassan. Autoplay test!", "gtts_testing_autoplay.mp3")












from elevenlabs.client import ElevenLabs
from elevenlabs import save
from pydub import AudioSegment
import subprocess
import platform
import os

def text_to_speech_with_elevenlabs(input_text, output_filepath_mp3):
    # Initialize the ElevenLabs client
    client = ElevenLabs(api_key="sk_57bc0ec633315fd9225f416d91570480326a25bb7e934623")

    # Get voice named "Aria"
    voices = client.voices.get_all().voices
    voice = next((v for v in voices if v.name.lower() == "aria"), None)

    if voice is None:
        raise ValueError("Voice 'Aria' not found. Please check available voices.")

    # Generate MP3 audio
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id=voice.voice_id,
        model_id="eleven_turbo_v2",
        output_format="mp3_22050_32"
    )

    # Save MP3 file
    save(audio, output_filepath_mp3)

    # Convert MP3 to WAV
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(output_filepath_mp3)
    sound.export(output_filepath_wav, format="wav")

    # Autoplay the WAV audio based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath_wav])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

from deep_translator import GoogleTranslator

from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from pydub import AudioSegment
import platform
import subprocess

def multilingual_tts_response(text, language_code, output_filepath_mp3="final.mp3"):
    # Translate from English to target language
    translated_text = GoogleTranslator(source='en', target=language_code).translate(text)
    
    # Generate audio
    tts = gTTS(text=translated_text, lang=language_code, slow=False)
    tts.save(output_filepath_mp3)

    # Convert MP3 to WAV
    output_filepath_wav = output_filepath_mp3.replace(".mp3", ".wav")
    sound = AudioSegment.from_mp3(output_filepath_mp3)
    sound.export(output_filepath_wav, format="wav")

    # Autoplay based on OS
    os_name = platform.system()
    try:
        if os_name == "Darwin":
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":
            subprocess.run(['aplay', output_filepath_wav])
        else:
            print("Unsupported OS for autoplay.")
    except Exception as e:
        print(f"Audio playback error: {e}")

    return output_filepath_mp3


# Example usage
#text_to_speech_with_elevenlabs("Hello, this is your AI Doctor speaking.", "elevenlabs_testing.mp3")












