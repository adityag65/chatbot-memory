import os
from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)


# System personality
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a friendly, helpful, and concise AI assistant. "
        "Answer clearly and naturally."
    )
}


# Conversation memory
messages = [SYSTEM_MESSAGE]


# Keep the system message + last 5 conversation messages
MAX_MESSAGES = 5


def get_ai_response():
    """Send conversation history to Groq and return the AI response."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
    )

    return response.choices[0].message.content


def main():
    print("=" * 45)
    print("        AI CHATBOT WITH MEMORY")
    print("=" * 45)
    print("Type 'exit' to quit.")
    print("The chatbot remembers the last 5 messages.")
    print()

    while True:
        user_input = input("You: ").strip()

        # Exit command
        if user_input.lower() == "exit":
            print("\nAI: Goodbye! 👋")
            break

        # Ignore empty input
        if not user_input:
            print("AI: Please type something.")
            continue

        # Add user message to memory
        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            # Get AI response
            assistant_reply = get_ai_response()

            print(f"AI: {assistant_reply}\n")

            # Add AI response to memory
            messages.append({
                "role": "assistant",
                "content": assistant_reply
            })

            # Keep only system message + last 5 messages
            if len(messages) > MAX_MESSAGES + 1:
                messages[:] = [SYSTEM_MESSAGE] + messages[-MAX_MESSAGES:]

        except Exception as e:
            print(f"AI: Sorry, something went wrong: {e}\n")


if __name__ == "__main__":
    main()