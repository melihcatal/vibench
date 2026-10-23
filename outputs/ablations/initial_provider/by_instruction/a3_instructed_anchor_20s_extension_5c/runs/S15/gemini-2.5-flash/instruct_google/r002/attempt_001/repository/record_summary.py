import google.generativeai as genai
import os

def record_summary(documents: list[dict]):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    document_texts = []
    for i, doc in enumerate(documents):
        document_texts.append(f"Document {i+1}:\n{doc}\n")

    prompt = "Please summarize the following documents:\n\n" + "\n---\n".join(document_texts)
    
    response = model.generate_content(prompt)
    return {"status": "success", "summary": response.text}