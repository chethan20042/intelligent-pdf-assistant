
import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# ----------------------------------
# GEMINI CONFIGURATION
# ----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ----------------------------------
# GENERATE AI ANSWER
# ----------------------------------

def generate_answer(question, context):

    prompt = f"""
You are an intelligent conversational PDF assistant.

Your task is to answer questions using information from the
uploaded PDF and the previous conversation.

INSTRUCTIONS:

1. Carefully read the previous conversation and PDF context.

2. Understand follow-up questions using the previous conversation.
   For example, if the user asks "What is step 3?",
   identify which procedure they were discussing.

3. Use the uploaded PDF as the source of factual information.

4. Use relevant information even if it explains a related concept
   rather than using the exact words in the question.

5. If the PDF provides a partial answer, explain what it supports.

6. Do not invent facts or use outside knowledge to fill gaps.

7. If the PDF does not contain enough information,
   clearly say that the answer is not available in the document.

8. Keep the answer clear and beginner-friendly.

9. Mention relevant page numbers when possible.

10. If the current question cannot be understood from the
    conversation or PDF context, ask the user to clarify.

CONTEXT:
{context}

CURRENT USER QUESTION:
{question}

ANSWER:
"""

    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt
    )

    return response.output_text
