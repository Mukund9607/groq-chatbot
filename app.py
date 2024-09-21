import streamlit as st
from llm.llm_integration import Chatbot
from dotenv import load_dotenv
import os
import getpass
import uuid 
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from langchain_groq import ChatGroq
with st.sidebar:
    st.title('🤗💬 SportChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model
    
    💡 Note: No API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')
    # Display message history
    if st.button("Show Conversation History"):
    # Loop through the stored conversation and display each message
        for message in st.session_state["conversation_history"]:
            if message["role"] == "user":
                st.write(f"User: {message['content']}")
            else:
                st.write(f"Bot: {message['content']}")
# Load environment variables
chatbot = Chatbot()




# Set up Streamlit session state
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = []

# Streamlit page setup
st.title("LangChain Chatbot with Session-based Message History (Groq API)")


# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# # Input form for user input
# user_input = st.text_input("You:")

if user_input:= st.chat_input("What is up?"):
    st.session_state["conversation_history"].append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        # Get chatbot response for the current session
        response = chatbot.get_response(user_input, session_id=st.session_state["session_id"])
        st.write(response)
    # Append user input and bot response to session state history
    st.session_state.messages.append({"role": "bot", "content": response})
    st.session_state["conversation_history"].append({"role": "bot", "content": response})
    
    
    # # Show the bot's response immediately after user input
    # st.write(f"Bot: {response}")


