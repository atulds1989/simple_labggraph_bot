import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict


# Load environment variables from the .env file
load_dotenv()

# Set up API keys from environment variables
groq_api_key = os.getenv("GROQ_API_KEY")
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")

# Initialize LangChain Groq model
llm = ChatGroq(groq_api_key=groq_api_key, model_name="Gemma2-9b-It")

# Define state structure for LangGraph
class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Define chatbot function that handles the conversation state
def chatbot(state: State):
    return {"messages": llm.invoke(state['messages'])}

# Build the state machine graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()


# Streamlit interface
st.title("LangGraph Chatbot")


# Create a text input box for user input
user_input = st.text_input("You:", "")

# Store the chat history in session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if user_input:
    # Add user input to the conversation
    st.session_state['messages'].append(("user", user_input))

    # Run the chatbot state machine and get the response
    for event in graph.stream({'messages': st.session_state['messages']}):
        for value in event.values():
            bot_response = value['messages'].content
            st.session_state['messages'].append(("assistant", bot_response))
    
    # Display the conversation history
    for speaker, message in st.session_state['messages']:
        if speaker == "user":
            st.markdown(f"**You**: {message}")
        else:
            st.markdown(f"**Assistant**: {message}")

# Optionally, provide an option to clear the chat
if st.button("Clear Chat"):
    st.session_state['messages'] = []


# while True:
#   user_input=input("User: ")
#   if user_input.lower() in ["quit","q"]:
#     print("Good Bye")
#     break
#   for event in graph.stream({'messages':("user",user_input)}):
#     print(event.values())
#     for value in event.values():
#       print(value['messages'])
#       print("Assistant:",value["messages"].content)


def footer():

    st.markdown("---")
    st.markdown("### About")
    st.markdown("This is a question answering agent using Langsmith and LangGraph you can ask anything...")
    st.markdown("Developed by Atul Purohit")

footer()


