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
# st.title("💬 Interactive Chatbot")

# Streamlit interface
st.markdown(
    "<h3 style='text-align: center; color: #333;'>💬 Interactive Chatbot</h3>",
    unsafe_allow_html=True,
)

# Sidebar information
with st.sidebar:
    st.subheader("🤖 Chatbot Information")
    st.write("This chatbot provides intelligent responses by either using an AI assistant Developed on LangGraph/LangSmith ")
    st.write("Sources used will be shown next to responses, enabling a clear understanding of where each answer originates from.")



# Store chat history in session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []


# Display chat history with bubble-style UI
def display_chat():
    st.markdown("###### Chat History")
    for speaker, message in st.session_state['messages']:
        if speaker == "user":
            st.markdown(
                f"<div style='background-color:#DCF8C6; border-radius:15px; padding:8px; margin:5px 0; text-align:right;'>"
                f"<strong>You:</strong> {message}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div style='background-color:#F1F0F0; border-radius:15px; padding:8px; margin:5px 0; text-align:left;'>"
                f"<strong>Assistant:</strong> {message}</div>",
                unsafe_allow_html=True,
            )

# Display chat history
# display_chat()

# Input section at the bottom with arrow button in the same row
st.markdown("---")
with st.form(key="input_form", clear_on_submit=True):
    cols = st.columns([10, 1])  # Creates two columns: input and submit button
    user_input = cols[0].text_input("", label_visibility="collapsed", placeholder="Type your message here...")  
    submit_button = cols[1].form_submit_button("➤")  # Arrow button for submit

# Process input and update chat
if submit_button and user_input:
    # Add user input to the conversation
    st.session_state['messages'].append(("user", user_input))

    # Run the chatbot state machine and get the response immediately
    response = None
    for event in graph.stream({'messages': st.session_state['messages']}):
        for value in event.values():
            response = value['messages'].content  # Store the response message
            st.session_state['messages'].append(("assistant", response))  # Add response to session state

    # Display the updated chat history with new messages
    display_chat()

# Clear chat button below input section for better accessibility
if st.button("Clear Chat", help="Clear the entire chat history"):
    st.session_state['messages'] = []
    st.experimental_rerun()  # Reload to refresh chat display

# Footer section
def footer():
    st.markdown("---")
    st.markdown("### About")
    st.markdown("This chatbot is built using Langsmith and LangGraph. Enjoy interactive conversations!")
    # st.markdown("Developed by **Atul Purohit**")

# Display footer
footer()
