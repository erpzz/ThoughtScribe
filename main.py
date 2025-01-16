# Developer: Eric Neftali Paiz
import streamlit as st
from elevenlabs.client import ElevenLabs
from text_extraction import extract_text_from_pdf, save_uploaded_file
from voice_generation import generate_speech, get_voices, create_agent
from dotenv import load_dotenv
import os, requests
import io
from elevenlabs.conversational_ai.conversation import Conversation
from util import *
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
import streamlit.components.v1 as components


st.set_page_config(
    page_title="ThoughtScribe",          
    page_icon="images/favicon.png",    
)

load_dotenv()
agent_id = os.getenv("AGENT_ID")
user_settings = load_user_settings()
st.session_state.update(user_settings)
def reload_page():
    components.html(
        """
        <script>
            window.location.reload();
        </script>
        """,
        height=0,
    )
if not st.session_state.get("api_key"):
    st.session_state["api_key"] = os.getenv("ELEVENLABS_API_KEY", "").strip()

if not st.session_state.get("agent_id"):
    st.session_state["agent_id"] = os.getenv("AGENT_ID", "").strip()
def update_env_file(api_key, agent_id):
    """
    Update or create the .env file with the given API key and Agent ID.
    
    Args:
        api_key (str): The ElevenLabs API key.
        agent_id (str): The newly created Agent ID.
    """
    env_file_path = ".env"
    lines_to_write = []
    
    if os.path.exists(env_file_path):
        with open(env_file_path, "r") as file:
            lines = file.readlines()

        found_api_key = False
        found_agent_id = False
        for line in lines:
            if line.startswith("ELEVENLABS_API_KEY="):
                lines_to_write.append(f"ELEVENLABS_API_KEY={api_key}\n")
                found_api_key = True
            elif line.startswith("AGENT_ID="):
                lines_to_write.append(f"AGENT_ID={agent_id}\n")
                found_agent_id = True
            else:
                lines_to_write.append(line)

        if not found_api_key:
            lines_to_write.append(f"ELEVENLABS_API_KEY={api_key}\n")
        if not found_agent_id:
            lines_to_write.append(f"AGENT_ID={agent_id}\n")
    else:
        lines_to_write = [
            f"ELEVENLABS_API_KEY={api_key}\n",
            f"AGENT_ID={agent_id}\n"
        ]

    with open(env_file_path, "w") as file:
        file.writelines(lines_to_write)
    print(f".env file updated successfully at {env_file_path}")
def create_agent(api_key, agent_name, voice_id, llm, system_prompt):
    url = "https://api.elevenlabs.io/v1/convai/agents/create"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "conversation_config": {
            "agent": {
                "prompt": {
                    "prompt": system_prompt,
                    "llm": llm,
         
                },
                "first_message": "You decided to come vent? Tell me, what's on your mind?",
                "language": "en" 
            }
        },
        "name": agent_name,
        "default_voice_id": voice_id
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["agent_id"]
    else:
        raise Exception(f"Failed to create agent: {response.text}")



def load_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except Exception as e:
        st.error(f"Error loading file '{file_path}': {e}")
        return ""

def agent_setup():
    st.title("ThoughtScribe Agent Setup")
    st.subheader("Configure and Create Your ThoughtScribe Agent")
    api_key = st.text_input(
        "ElevenLabs API Key:",
        type="password",
        value=st.session_state.get("api_key", ""),
        on_change=lambda: st.session_state.update({"show_api_warning": False})
    )

    if not api_key.strip():
        st.session_state["show_api_warning"] = True
        st.error("Missing ElevenLabs API key. Please check your .env file or input it above.")
        return 
    try:
        client = ElevenLabs(api_key=api_key)
        voice_choices = [voice["Name"] for voice in get_voices(client)]
        st.session_state["show_api_warning"] = False
    except Exception as e:
        st.error(f"Invalid or missing API key. Unable to fetch voices: {e}")
        return 

    agent_name = st.text_input("Agent Name:", value="Custom Agent")

    client = ElevenLabs(api_key=api_key)
    
    voice_choices = [voice["Name"] for voice in get_voices(client)]

    llm_choices = [
    "claude-3-5-sonnet",
    "claude-3-haiku",
    "custom-llm",
    "gemini-1.0-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o"
]
    if "selected_voice" not in st.session_state:
        st.session_state["selected_voice"] = voice_choices[0]

    if "selected_llm" not in st.session_state:
        st.session_state["selected_llm"] = llm_choices[0]
    selected_voice = st.selectbox("Choose a Default Voice:", options=voice_choices, key="selected_voices")
    selected_llm = st.selectbox("Choose LLM:", options=llm_choices, key="selected_llm", index=llm_choices.index(st.session_state["selected_llm"]))

    knowledge_base_path = "ThoughtScribe_Context/Mental_Health_Retrieval.txt"
    knowledge_base_content = load_file_content(knowledge_base_path)
    knowledge_base = [
    {
        "type": "text",
        "name": "Mental Health Support",
        "id": "knowledge_base_001",
        "content": "ThoughtScribe_Context/Mental_Health_Retrieval.txt"
    }
]

    system_prompt_path = "ThoughtScribe_Context/system_prompt.txt"
    system_prompt_content = load_file_content(system_prompt_path)
    # st.write(f"Assigned Knowledge Base: {knowledge_base_content}")
    # st.write(f"Assigned System Prompt: {system_prompt_content}")
    # Create Agent Button
    if st.button("Create Agent"):
        try:
            agent_id = create_agent(
                api_key=api_key,
                agent_name=agent_name,
                voice_id=selected_voice,
                llm=selected_llm,
                # knowledge_base=knowledge_base,
                system_prompt=system_prompt_content,
            )
            
            if st.button("Create Agent"):
                try:
                    agent_id = create_agent(
                        api_key=api_key,
                        agent_name=agent_name,
                        voice_id=selected_voice,
                        llm=selected_llm,
                        system_prompt=system_prompt_content,
                    )

                    if create_agent:
                        st.session_state["agent_id"] = agent_id
                        st.session_state["api_key"] = api_key
                        update_env_file(api_key, agent_id)
                        st.success("New agent created successfully and saved to .env file!")
                    else:
                        st.session_state["agent_id"] = agent_id
                        st.session_state["api_key"] = api_key
                        st.success("New agent created successfully!")

                except Exception as e:
                    st.error(f"Error creating agent: {e}")
        except Exception as e:
                st.error(f"Error creating agent: {e}")


if "api_key" not in st.session_state or "agent_id" not in st.session_state:
    agent_setup()
if not st.session_state.get("api_key") or not st.session_state.get("agent_id"):
    st.warning("You must set up an ElevenLabs account & create an API key to use with this project.")
    agent_setup()

def get_api_key_and_agent_id():
    """
    Retrieves the API key and agent ID from session state, saved settings, or environment variables.

    Returns:
        tuple: (api_key, agent_id)
    """
    api_key = st.session_state.get("api_key")
    agent_id = st.session_state.get("agent_id")

    # Check saved settings next
    if not api_key or not agent_id:
        saved_settings = load_user_settings()
        api_key = saved_settings.get("api_key", api_key)
        agent_id = saved_settings.get("agent_id", agent_id)


    if not api_key:
        api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    if not agent_id:
        agent_id = os.getenv("AGENT_ID", "").strip()

    return api_key, agent_id


if not st.session_state["agent_id"]:
    st.warning("Agent ID is missing. Please fetch or set up an agent.")
    
    
    if st.button("Fetch or Setup Agent"):
        try:
           
            api_key, agent_id = get_api_key_and_agent_id()

            
            if not api_key:
                st.error("API key is missing. Please configure it in the settings or .env file.")
                st.stop()

            if not agent_id:
                st.warning("No agent ID found. Please create an agent or enter an existing ID.")
                agent_name = st.text_input("Agent Name:", value="Custom Agent")
                agent_description = st.text_area("Agent Description:", value="This is a dynamically created agent.")

                if st.button("Create New Agent"):
                    
                    try:
                        agent_id = create_agent(api_key, agent_name, agent_description)
                        st.session_state["agent_id"] = agent_id
                        st.session_state["api_key"] = api_key
                        save_user_settings({"api_key": api_key, "agent_id": agent_id})
                        st.success(f"Agent created successfully!")
                    
                    except Exception as e:
                        st.error(f"Error creating agent: {e}")

                # Allow manual entry of existing agent ID
                manual_agent_id = st.text_input("Or Enter Existing Agent ID:")
                if st.button("Use Existing Agent"):
                    if manual_agent_id.strip():
                        st.session_state["agent_id"] = manual_agent_id.strip()
                        st.session_state["api_key"] = api_key
                        save_user_settings({"api_key": api_key, "agent_id": manual_agent_id.strip()})
                        st.success(f"Using existing agent ID: {manual_agent_id}")
                    else:
                        st.error("Please enter a valid Agent ID.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.success(f"Agent loaded in!")

api_key = st.session_state["api_key"]
agent_id = st.session_state["agent_id"]

client = ElevenLabs(api_key=api_key)


elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

api_key = os.getenv


client = ElevenLabs(api_key=elevenlabs_api_key)
with st.sidebar:
    st.title("ThoughtScribe")
    st.info("Turn your documents into insightful conversations and audio experiences with ThoughtScribe.")
    view_mode = st.radio("Choose the view mode:", ["Notes to Speech", "After Class Venting"])

col1, col2 = st.columns([1, 3])
with col1:
    st.image("images/thoughtscribe_logo.png", caption=None, use_container_width=True)
with col2:
    st.title("ThoughtScribe")
    st.subheader("Your AI-Powered Document Narrator")
    st.caption("Where your documents speak and think.")

st.markdown("---")


if view_mode == "Notes to Speech":
    st.header("Text Processing and Voice Generation")

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        file_path = save_uploaded_file(uploaded_file)
        extracted_text = extract_text_from_pdf(file_path)
        st.text_area("Extracted Text", value=extracted_text, height=200)
        
        voice_name = st.selectbox("Choose a voice", [v["Name"] for v in get_voices(client)])
        
        if "summary" not in st.session_state:
            st.session_state["summary"] = None  
        
        if st.button("Summarize"):
            
            try:
                from ollama_integration import OllamaIntegration
                ollama_client = OllamaIntegration(base_url=ollama_base_url)
                with st.spinner("Generating summary..."):
                    summary = ollama_client.summarize_text(extracted_text)
                st.session_state["summary"] = summary 
                st.text_area("Summary", value=summary, height=150)
            except Exception as e:
                st.error(f"An error occurred while summarizing: {e}")
        voice_name_summary = st.selectbox(
            "Choose a voice for summary", 
            [v["Name"] for v in get_voices(client)], 
            key="summary_voice_select_key"
        )
    
        if st.button("Generate Speech for Summary"):
            if st.session_state["summary"]:
                with st.spinner("Converting summary to audio..."):
                    try:
                        voice_name = st.selectbox(
                            "Choose a voice for summary", 
                            [v["Name"] for v in get_voices(client)], 
                            key="summary_voice_select" 
                        )
                        summary_audio = generate_speech(client, st.session_state["summary"], voice_name)
                        summary_audio = b"".join(summary_audio)  
                        
                        st.download_button(
                            label="Download Summary Audio",
                            data=io.BytesIO(summary_audio),
                            file_name="summary_audio.mp3",
                            mime="audio/mpeg"
                        )
                        st.audio(summary_audio, format="audio/mp3")
                    except Exception as e:
                        st.error(f"An error occurred while generating speech: {e}")
            else:
                st.warning("Please generate a summary first.")

        if st.button("Generate Speech"):
            with st.spinner("Converting text to audio. Please wait..."):
                try:
                    voice_name = st.selectbox(
                        "Choose a voice for full text", 
                        [v["Name"] for v in get_voices(client)], 
                        key="full_text_voice_select"  
                    )
                    branding_intro = "This audio is brought to you by ThoughtScribe, powered by ElevenLabs."
                    branding_audio = generate_speech(client, branding_intro, voice_name)
                    branding_audio = b"".join(branding_audio)

                    user_audio = generate_speech(client, extracted_text, voice_name)
                    user_audio = b"".join(user_audio)

                    complete_audio = branding_audio + user_audio

                    st.download_button(
                        label="Download Audio",
                        data=complete_audio,
                        file_name="final_output.mp3",
                        mime="audio/mpeg"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if view_mode == "After Class Venting":
    st.header("ThoughtScribe Friend")
    st.caption("Come talk or vent about school work after studying.")
    if st.button("Create New Agent"):
            agent_setup()
    if "conversation" not in st.session_state:
        st.session_state["conversation"] = None 

    if st.button("Start Conversation"):
        try:
            api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
            agent_id = os.getenv("AGENT_ID", "").strip()

            if not api_key or not agent_id:
                st.error("Missing API key or Agent ID. Please check your .env file.")
                st.stop()

            client = ElevenLabs(api_key=api_key)
            status_message = st.empty() 
            status_message.write("Initializing Conversation...")

            conversation = Conversation(
                client=client,
                agent_id=agent_id,
                requires_auth=bool(api_key),
                audio_interface=DefaultAudioInterface(),
                callback_agent_response=lambda response: st.write(f"**Agent:** {response}"),
                callback_user_transcript=lambda transcript: st.write(f"**You:** {transcript}"),
            )
            conversation.start_session()
            status_message.empty()  
            st.success("Conversation started! Speak into your microphone.")

            st.session_state["conversation"] = conversation

        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.session_state["conversation"] and st.button("End Conversation", key="end_convo"):
        try:
            conversation = st.session_state["conversation"]
            with st.spinner("Ending the conversation..."):
             
                conversation.end_session()
             
                conversation_ended = conversation.wait_for_session_end()
                if conversation_ended:
                    st.success("Conversation successfully ended.")
                else:
                    st.warning("Some threads might still be active.")

            st.session_state["conversation"] = None
            st.empty()

        except Exception as e:
            st.error(f"Failed to end the conversation: {e}")


st.markdown("---")
st.markdown("**ThoughtScribe** © 2025 | Made with ❤️ by Eric Neftali Paiz")
