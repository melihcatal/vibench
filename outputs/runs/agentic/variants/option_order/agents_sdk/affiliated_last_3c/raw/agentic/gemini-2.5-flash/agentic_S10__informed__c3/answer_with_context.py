import google.generativeai as genai
import os

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (Google Gemini) to answer a question using provided context.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Given the following context, answer the question.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text
