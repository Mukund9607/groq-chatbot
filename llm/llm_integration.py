import getpass
import os
from langchain.schema import AIMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
# Prompt for Groq API key securely


api_key = os.getenv("GROQ_API_KEY")
if api_key is None:
    raise ValueError("GROQ_API_KEY not set. Please check your .env file or environment variables.")
model = ChatGroq(model="llama3-8b-8192", api_key=api_key)
from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory

# Initialize Groq's llama model
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.prompts import PromptTemplate
import requests

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    # If the session doesn't exist, create a new chat history
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

class Chatbot:
    def __init__(self):
        self.model = model
        self.with_message_history = RunnableWithMessageHistory(self.model, get_session_history)
        
        # Memory to store message history
        # Define prompt template
        # self.prompt = PromptTemplate(
        #     input_variables=["history", "input"],
        #     template="You are a sports expert. Here is the conversation so far: {history}. The user asked: {input}. Respond appropriately."
        # )
        
    
    def get_response(self, user_input, session_id):
        # Get the conversation history for the session
        history = get_session_history(session_id)
        prompt = f"You are a sports expert. Here is the conversation so far: {history}. The user asked: {user_input}. Respond appropriately."
        print({session_id})
        # Get response from Groq's model with the message history
        response = self.with_message_history.invoke(
            {None: prompt},  # The prompt for the model
            {'configurable': {'session_id': session_id}}
            )
        
        # Save the input and response to the conversation history
        history.add_message(HumanMessage(content=user_input))  # Use HumanMessage to store the user input
        history.add_message(AIMessage(content=response.content))  # Use AIMessage to store the bot response
        
        return response.content

    def get_message_history(self, session_id):
        """Retrieve the chat history for display."""
        history = get_session_history(session_id)
        messages = history.messages  # Assuming this returns a list of stored messages
        # print({message})    
        # Format the history for display
        formatted_history = []
        for message in messages:
            if isinstance(message, HumanMessage):
                formatted_history.append(f"User: {message.content}")
            elif isinstance(message, AIMessage):
                formatted_history.append(f"Bot: {message.content}")
            else:
                raise ValueError(f"Got unsupported message type: {message}")
    
        return "\n".join(formatted_history)
