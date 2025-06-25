# utils.py

from deep_translator import GoogleTranslator
from groq import Groq
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Detect language of text using translation service
def detect_language(text):
    try:
        lang = GoogleTranslator(source='auto', target='en').detect(text)
        return lang
    except Exception as e:
        print(f"[Language Detection Error]: {e}")
        return "en"

# Use Groq LLM without image (text-only)
def ask_doctor_llm(text_prompt):
    client = Groq(api_key=GROQ_API_KEY)

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a medical expert."},
            {"role": "user", "content": text_prompt},
        ],
        temperature=0.7
    )

    return completion.choices[0].message.content
