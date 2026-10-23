import google.generativeai as genai
import os

def answer_question_with_context(question: str, context: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Using the following context, answer the question:

Context: {context}

Question: {question}

Answer:"
    response = model.generate_content(prompt)
    return response.text
