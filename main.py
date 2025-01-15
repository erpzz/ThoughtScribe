# Developer: Eric Paiz
import streamlit as st
from elevenlabs.client import ElevenLabs
from ollama_integration import OllamaIntegration
from text_extraction import extract_text_from_pdf, save_uploaded_file
from voice_generation import generate_speech, get_voices
from dotenv import load_dotenv
import streamlit.components.v1 as components
import os
import signal 
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface
from streamlit_lottie import st_lottie

load_dotenv()
agent_id = os.getenv("AGENT_ID")
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

api_key = os.getenv
if not elevenlabs_api_key:
    st.error("Missing ElevenLabs API key. Please check your .env file.")
    st.stop()

client = ElevenLabs(api_key=elevenlabs_api_key)
ollama_client = OllamaIntegration(base_url=ollama_base_url)


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
                            data=summary_audio,
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
                callback_agent_response_correction=lambda original, corrected: st.write(
                    f"**Agent Correction:** {original} -> {corrected}"
                ),
                callback_user_transcript=lambda transcript: st.write(f"**You:** {transcript}"),
            )
            conversation.start_session()
            status_message.empty()  
            st.success("Conversation started! Speak into your microphone.")

            if st.button("End Conversation by saying End Conversation", key="end_convo"):
                try:
                    conversation.end_session()
                    conversation_ended = conversation.wait_for_session_end(timeout=5)
                    if conversation_ended:
                        st.success("Conversation successfully ended.")
                    else:
                        st.warning("Some threads might still be active.")
                    gif_container.empty() 
                except Exception as e:
                    st.error(f"Failed to end the conversation: {e}")

        except Exception as e:
            st.error(f"An error occurred: {e}")


st.markdown("---")
st.markdown("**ThoughtScribe** © 2025 | Made with ❤️ by Eric Neftali Paiz")
