import gradio as gr
import os
from brain_of_the_doctor import analyze_image_with_query, encode_image
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import multilingual_tts_response

# Set the model
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def process_input(user_text, image, audio_file):
    user_display = ""
    translated_text = user_text
    language_code = "en"  # default

    # Handle audio
    if audio_file:
        try:
            audio_path = audio_file
            original_text, detected_lang, translated = transcribe_with_groq("whisper-large-v3", audio_path, os.environ.get("GROQ_API_KEY"))
            user_display = f"🗣️ Transcribed: {original_text} ({detected_lang})"
            translated_text = translated
            language_code = detected_lang
        except Exception as e:
            user_display = f"⚠️ Audio transcription error: {e}"
            translated_text = ""
    
    # Handle if only text
    elif user_text:
        user_display = f"📝 You said: {user_text}"
        translated_text = user_text

    # Now generate the AI response
    encoded_img = encode_image(image) if image else None
    try:
        ai_response = analyze_image_with_query(translated_text, GROQ_MODEL, encoded_image=encoded_img)
    except Exception as e:
        ai_response = f"⚠️ Error generating AI response: {e}"

    # Generate voice output
    audio_output_path = multilingual_tts_response(ai_response, language_code)

    return user_display, ai_response, audio_output_path

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧑‍⚕️ MediSage — Multimodal Medical Assistant")

    with gr.Row():
        text_input = gr.Textbox(label="Type your message (optional)", placeholder="Describe your issue or question")
        image_input = gr.Image(type="filepath", label="Upload image (optional)")
        audio_input = gr.Audio(type="filepath", label="Speak instead (optional)")

    with gr.Row():
        submit_btn = gr.Button("Submit")

    user_transcript_display = gr.Textbox(label="Patient's input", interactive=False)
    response_display = gr.Textbox(label="AI Doctor's response", interactive=False)
    audio_output = gr.Audio(label="Voice of the AI Doctor")

    submit_btn.click(
        fn=process_input,
        inputs=[text_input, image_input, audio_input],
        outputs=[user_transcript_display, response_display, audio_output]
    )

demo.launch()
