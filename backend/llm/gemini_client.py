from pathlib import Path
import os

from dotenv import load_dotenv
from google import genai

ROOT = Path(__file__).resolve().parent.parent.parent

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(
    api_key=API_KEY
)


def generate_answer(
    question: str,
    bible_context: str,
    denomination_prompt: str = "",
    history: str = ""
):

    prompt = f"""
You are a Christian AI Assistant.

STRICT RULES:

1. Use ONLY the Bible passages provided below.

2. Do NOT mention any scripture reference not present in the supplied context.

3. Do NOT invent Bible verses.

4. Do NOT use outside theological knowledge.

5. If context is insufficient, say:
"The provided Bible context does not contain enough information to answer fully."

Bible Context:

{bible_context}

Denomination Context:

{denomination_prompt}

Question:

Conversation History:

{history}

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text