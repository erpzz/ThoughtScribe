# Developer: Eric Neftali Paiz
from elevenlabs.client import ElevenLabs
import os

# Directory for saving generated audio files
AUDIO_OUTPUT_DIR = "data/audio"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

def get_voices(client):
    """
    Fetches available voices from ElevenLabs.

    Args:
        client: ElevenLabs client instance.

    Returns:
        list: A list of dictionaries with voice names and IDs.
    """
    if not isinstance(client, ElevenLabs):
        raise TypeError("Invalid client. Please provide a valid ElevenLabs client instance.")

    try:
        response = client.voices.get_all()
        return [{"Name": voice.name, "ID": voice.voice_id} for voice in response.voices]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch voices: {e}")

def generate_speech(client, text, voice_name, save_as=None):
    """
    Generates speech for the given text using a specified voice.

    Args:
        client: ElevenLabs client instance.
        text: The text to convert to speech.
        voice_name: The name of the voice to use.
        save_as: Optional filename to save the generated audio.

    Returns:
        bytes: Generated audio content.
    """
    if not isinstance(client, ElevenLabs):
        raise TypeError("Invalid client. Please provide a valid ElevenLabs client instance.")

    if not text.strip():
        raise ValueError("Input text cannot be empty.")

    voices = get_voices(client)
    voice_id = next((voice["ID"] for voice in voices if voice["Name"] == voice_name), None)

    if not voice_id:
        raise ValueError(f"Voice '{voice_name}' not found.")

    try:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_turbo_v2"
        )

        if save_as:
            save_path = os.path.join(AUDIO_OUTPUT_DIR, save_as)
            with open(save_path, "wb") as audio_file:
                audio_file.write(audio)
            print(f"Audio saved as: {save_path}")

        return audio
    except Exception as e:
        raise RuntimeError(f"Failed to generate speech: {e}")
