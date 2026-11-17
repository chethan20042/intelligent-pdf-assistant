
from rag_pipeline import ask_pdf_question


question = "What is image preprocessing?"

result = ask_pdf_question(question)

print("\nUSER QUESTION:")
print(result["question"])

print("\nAI ANSWER:")
print(result["answer"])

print("\nSOURCE PAGES:")

for source in result["sources"]:
    print("Page:", source["page"])
