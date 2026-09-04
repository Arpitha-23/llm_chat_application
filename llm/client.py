
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not configured in the .env file.")

client = genai.Client(api_key=API_KEY)


def get_ai_response(messages):
    """
    Send conversation history to Gemini using the Interactions API.
    """

    system_instruction = ""
    conversation = []

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role == "system":
            system_instruction = content

        elif role == "user":
            conversation.append(
                {
                    "type": "text",
                    "text": f"User: {content}"
                }
            )

        elif role == "assistant":
            conversation.append(
                {
                    "type": "text",
                    "text": f"Assistant: {content}"
                }
            )

    response = client.interactions.create(
        model="gemini-3.6-flash",
        input=conversation,
        system_instruction=system_instruction
    )

    return response.output_text

