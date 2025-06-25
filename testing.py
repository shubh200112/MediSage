from elevenlabs import play, save, Voice, VoiceSettings, set_api_key, generate

# Set your API key
set_api_key("sk_57bc0ec633315fd9225f416d91570480326a25bb7e934623")

# Generate speech
audio = generate(
    text="This is ElevenLabs speaking from Google Colab!",
    voice=Voice(
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Aria voice ID
        settings=VoiceSettings(stability=0.5, similarity_boost=0.75)
    ),
    model="eleven_turbo_v2"
)

# Save to MP3
save(audio, "output.mp3")
