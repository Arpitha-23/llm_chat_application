import streamlit as st
from llm.client import get_ai_response

st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chat Assistant")
st.write("Chat with an AI assistant powered by Gemini.")

# Load system prompt
with open("prompts/system_prompt.txt", "r", encoding="utf-8") as file:
    system_prompt = file.read()

# Initialize conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    st.rerun()

# Display conversation history
for message in st.session_state.messages:

    # Don't display system message
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = get_ai_response(
                    st.session_state.messages
                )

                # Display AI response
                st.markdown(response)

                # Save AI response to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response
                })

            except Exception as e:
                st.error(
                    f"Something went wrong: {e}"
                )