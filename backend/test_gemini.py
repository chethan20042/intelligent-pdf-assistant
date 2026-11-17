import time
from llm import client

try:
    print("Testing Gemini 3.5 Flash-Lite...")

    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input="Explain Artificial Intelligence in two sentences."
    )

    print("\nSUCCESS!")
    print(response.output_text)

except Exception as e:
    print("\nERROR:")
    print(e)