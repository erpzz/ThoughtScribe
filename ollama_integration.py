import requests
import os
from elevenlabs import ElevenLabs, Voice, VoiceSettings


class OllamaIntegration:
    def __init__(self, base_url="http://localhost:11434", elevenlabs_api_key=None):
        print("Initializing OllamaIntegration...")
        self.base_url = base_url
        self.session_id = None
        self.elevenlabs_client = ElevenLabs(api_key=elevenlabs_api_key) if elevenlabs_api_key else None

    

    def send_prompt(self, prompt, model="llama3.2"):
        print(f"Sending prompt to Ollama: {prompt[:50]}...")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],  # For /api/chat
            "stream": False
        }
        response = requests.post(f"{self.base_url}/api/chat", json=payload)
        if response.status_code == 200:
            return response.json().get("message", {}).get("content", "No response received.")
        else:
            print(f"Error sending prompt: {response.text}")
            raise RuntimeError(f"Failed to send prompt: {response.text}")


    def summarize_text(self, text):
        print("Generating summary for provided text...")
        summary_prompt = f"Please summarize the following text:\n{text}"
        return self.send_prompt(summary_prompt)


    def analyze_sentiment(self, text):
        print("Performing sentiment analysis...")
        sentiment_prompt = f"Analyze the sentiment of the following text:\n{text}"
        return self.send_prompt(sentiment_prompt)

    def enhanced_user_prompt(self, base_prompt, user_additions):
        print("Enhancing prompt with user instructions...")
        combined_prompt = f"{base_prompt}\n\nUser Additions: {user_additions}"
        print(f"Generated combined prompt: {combined_prompt[:50]}...")
        return combined_prompt

    def generate_notes_with_sentiment(self, text, user_additions=None):
        print("Generating notes with sentiment analysis...")
        sentiment = self.analyze_sentiment(text)
        notes_prompt = f"Generate detailed notes based on the sentiment:\n{sentiment}"
        if user_additions:
            notes_prompt = self.enhanced_user_prompt(notes_prompt, user_additions)
        return self.send_prompt(notes_prompt)

    def generate_audio_response(self, text, voice_name):
        print(f"Generating audio response for text: {text[:50]}... using voice: {voice_name}")
        if not self.elevenlabs_client:
            raise ValueError("ElevenLabs API key is not configured.")

        voices = self.elevenlabs_client.voices.get_all()
        voice_id = next((v.voice_id for v in voices if v.name == voice_name), None)

        if not voice_id:
            print(f"Voice '{voice_name}' not found.")
            raise ValueError(f"Voice '{voice_name}' not found.")

        try:
            audio = self.elevenlabs_client.generate(
                text=text,
                voice=Voice(
                    voice_id=voice_id,
                    settings=VoiceSettings(stability=0.7, similarity_boost=0.5)
                )
            )
            print("Audio generation successful.")
            return audio
        except Exception as e:
            print(f"Error generating audio: {e}")
            raise RuntimeError(f"Failed to generate speech: {e}")

    def save_audio(self, audio, filename="response_audio.mp3"):
        print(f"Saving audio to file: {filename}")
        output_dir = "data/audio"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        try:
            with open(file_path, "wb") as f:
                f.write(audio)
            print(f"Audio saved successfully at: {file_path}")
            return file_path
        except Exception as e:
            print(f"Error saving audio: {e}")
            raise RuntimeError(f"Failed to save audio: {e}")

    def summarize_and_generate_audio(self, text, voice_name):
        print("Summarizing text and generating audio...")
        summary = self.summarize_text(text)
        audio = self.generate_audio_response(summary, voice_name)
        return summary, audio


# Example Usage
if __name__ == "__main__":
    print("Starting main execution...")
    ollama = OllamaIntegration(elevenlabs_api_key="YOUR_ELEVENLABS_API_KEY")
    try:
        ollama.start_session()
        user_text = input("Enter text to analyze: ")
        summary = ollama.summarize_text(user_text)
        print(f"Summary:\n{summary}")

        use_audio = input("Generate an audio response? (yes/no): ").strip().lower()
        if use_audio == "yes":
            voice_name = input("Enter the ElevenLabs voice name: ")
            audio_content = ollama.generate_audio_response(summary, voice_name)
            audio_path = ollama.save_audio(audio_content)
            print(f"Audio saved at: {audio_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
