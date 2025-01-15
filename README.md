# ThoughtScribe

ThoughtScribe is a two-in-one tool designed to enhance productivity and support mental well-being. It allows users to turn notes into speech for easy review and provides a space to vent and have conversations with an AI-powered agent.

---

## Features

### 1. Notes to Speech
- Upload a PDF document.
- Extract and summarize the text.
- Generate audio for the full text or the summary to listen on the go.

### 2. After Class Venting
- Talk to an AI-powered agent that listens and responds in real-time.
- Vent about your day, share ideas, or just have a conversation.

---

## Built With
- **Python**: Core programming language.
- **Streamlit**: Web app framework.
- **ElevenLabs API**: For generating realistic AI speech.
- **Ollama**: Local LLM integration for summaries.
- **PyMuPDF (Fitz)**: PDF text extraction.
- **Docker**: Containerization for running locally.

---

## Setup Instructions

### Prerequisites
- **Python 3.10 or above** installed.
- **ElevenLabs API Key**: [Sign up here](https://elevenlabs.io) to get an API key.
- **Docker** (optional for containerized use).

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/thoughtscribe.git
   cd thoughtscribe
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up the `.env` File**
   - In the project root, create a file named `.env`.
   - Add your ElevenLabs API key and Agent ID:
     ```env
     ELEVENLABS_API_KEY=your_api_key_here
     AGENT_ID=your_agent_id_here
     ```
   - **Important**: Do not commit the `.env` file to version control to keep your credentials secure. Add `.env` to `.gitignore` if it isn’t already.

5. **Run the App**
   ```bash
   streamlit run main.py
   ```

6. **Access the App**
   Open your browser and go to `http://localhost:8501`.

---

## Secure Setup

- Use environment variables stored in the `.env` file to keep sensitive information (like API keys) secure.
- **Never share or commit the `.env` file.**
- If deploying to a remote server or cloud platform, configure environment variables through the hosting provider’s interface.

---

## How to Use

### Notes to Speech
1. Navigate to **Notes to Speech**.
2. Upload a PDF file.
3. Extract or summarize the text.
4. Generate and download the audio.

### After Class Venting
1. Navigate to **After Class Venting**.
2. Click on `Start Conversation`.
3. Speak into your microphone to start interacting.
4. Click `End Conversation` when done to stop the session.

---

## Future Plans
- Add mobile app support.
- Integrate more advanced sentiment analysis.
- Enable multilingual capabilities for non-English users.

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
