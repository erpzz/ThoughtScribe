# ThoughtScribe

ThoughtScribe is a multi-functional tool designed to boost productivity and support mental well-being. It allows users to convert notes into speech for easy review and provides a space to vent and have meaningful conversations with an AI-powered agent.

## Features

### 1. **Notes to Speech**
- Upload a PDF document.
- Extract and summarize the text.
- Generate audio for the full text or the summary to listen on the go.

### 2. **After Class Venting**
- Interact with an AI-powered agent that listens and responds in real-time.
- Share your thoughts, ideas, or just have a friendly chat.
- Create your own conversational agent dynamically with custom configurations, including personality, model, and knowledge base.

---

## Built With
- **Python**: Core programming language.
- **Streamlit**: Web app framework.
- **ElevenLabs API**: For generating realistic AI speech.
- **Ollama**: Local LLM integration for summaries.
- **PyMuPDF (Fitz)**: PDF text extraction.
- **Docker**: For containerized deployments.

---

## Setup Instructions

### Prerequisites
- **Python 3.10 or above**: Ensure Python is installed and added to your system's PATH.
- **ElevenLabs API Key**: [Sign up here](https://elevenlabs.io/) to create an account and obtain your API key.
  - This API key is required for generating speech and creating agents.
- **Docker** (optional): For containerized deployments.

### Installation

#### 1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/thoughtscribe.git
cd thoughtscribe
```

#### 2. **Create a Virtual Environment**
```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

#### 3. **Install Requirements**
```bash
pip install -r requirements.txt
```

#### 4. **Set Up the `.env` File**
- In the project root, create a file named `.env`.
- Add the following variables to configure your ElevenLabs API key and optionally a default agent ID:
```env
ELEVENLABS_API_KEY=your_api_key_here
AGENT_ID=your_agent_id_here  # Optional
```
- If you don’t already have an ElevenLabs API key, visit [ElevenLabs](https://elevenlabs.io/) to sign up and generate your key.

> **Important**: Do not share or commit the `.env` file to version control. Ensure `.env` is added to your `.gitignore` file to protect sensitive credentials.

### Dynamic Agent Creation
- If no agent is pre-configured, you can dynamically create one within the app by providing:
  - A valid API key.
  - An agent name.
  - Model preferences (e.g., GPT-4, Claude-3.5).
  - Optional settings such as knowledge base files and system prompts.

### Running the App
```bash
streamlit run main.py
```

### Access the App
- Open your browser and navigate to [http://localhost:8501](http://localhost:8501).

---

## Secure Setup
- **Environment Variables**: Store sensitive information like API keys in the `.env` file.
- **Avoid Sharing Credentials**: Never share or upload the `.env` file.
- **Remote Deployments**: Configure environment variables using your hosting provider's interface for additional security.
- **Encryption**: API keys are securely stored and handled within the application.

---

## How to Use

### 1. **Notes to Speech**
- Ensure an agent is loaded or created.
- Navigate to **Notes to Speech**.
- Upload a PDF file.
- Extract or summarize the text.
- Generate and download the audio for the full text or summary.

### 2. **After Class Venting**
- Ensure an agent is loaded or created.
- Navigate to **After Class Venting**.
- Click **Start Conversation**.
- Speak into your microphone to start interacting.
- Optionally, create your own agent by providing an API key, model, and personality.
- Click **End Conversation** when done to stop the session.

### 3. **Dynamic Agent Creation**
- If no agent is loaded, the app will prompt you to create one.
- Provide the following:
  - API Key
  - Agent Name
  - Default Voice
  - LLM Model (e.g., GPT-4, Claude-3.5)
  - Optional: Knowledge base (upload files or URLs) and system prompt.
- Once the agent is created, the app will automatically reload to enable full functionality.

---

## Future Plans
- Add mobile app support.
- Integrate advanced sentiment analysis.
- Enable multilingual capabilities for non-English users.
- Add SMS integration to ThoughtScribe conversational agents.

---

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

---

Thank you for using ThoughtScribe! We hope this tool helps you stay productive and feel supported in your day-to-day life.

