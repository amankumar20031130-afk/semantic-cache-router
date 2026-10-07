import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_llm(query: str, model: str):

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise AI assistant. "
                    "Answer clearly and directly. "
                    "Use short paragraphs and bullet points when useful. "
                    "Avoid unnecessary history, repetition, and overly long explanations."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        temperature=0.2
    )

    return {
        "answer": response.choices[0].message.content,
        "input_tokens": response.usage.prompt_tokens,
        "output_tokens": response.usage.completion_tokens
    }