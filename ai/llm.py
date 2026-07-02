import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_gemini(prompt: str) -> str:
    """
    Sends a prompt to Gemini and returns the generated text.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text


if __name__ == "__main__":
    print(ask_gemini("In one sentence, explain why SQL is important."))