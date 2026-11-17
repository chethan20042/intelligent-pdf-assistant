
from rag_pipeline import ask_pdf_question

question = "What is image processing?"

result = ask_pdf_question(question)

print("\nUSER QUESTION:")
print(result["question"])

print("\nAI ANSWER:")
print(result["answer"])

print("\nSOURCE PAGES:")

for source in result["sources"]:
    print(f"Page: {source['page']}")
