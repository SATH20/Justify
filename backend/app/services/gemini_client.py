
def generate_raw_llm(prompt: str) -> str:
    """
    Directly call Gemini with a custom prompt and return the raw text output.
    """
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, "text") else str(response)
import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted, NotFound

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ✅ Stable, supported model
model = genai.GenerativeModel("gemini-2.0-flash")


def generate_llm_response(user_query: str, rag_context: list) -> str:

    # Build legal context
    context_str = "\n".join(
        [
            f"Law: {item.get('law', '')}\nText: {item.get('text', '')}"
            for item in rag_context
        ]
    )

    prompt = f"""
You are a legal reasoning assistant.

Rules:
- Use ONLY the provided legal context.
- Do NOT invent laws or facts.
- Be neutral and bias-aware.
- If the context is insufficient, clearly state uncertainty.

User Query:
{user_query}

Legal Context:
{context_str}

Provide a clear explanation.
"""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()

    except ResourceExhausted:
        return (
            "The AI reasoning service is temporarily unavailable due to usage limits. "
            "Based on the retrieved legal information above, this issue may relate to the listed laws. "
            "Please try again later for a detailed explanation."
        )

    except NotFound:
        return (
            "The AI model is currently unavailable. "
            "Relevant legal information was retrieved, but detailed reasoning cannot be generated at this moment."
        )
