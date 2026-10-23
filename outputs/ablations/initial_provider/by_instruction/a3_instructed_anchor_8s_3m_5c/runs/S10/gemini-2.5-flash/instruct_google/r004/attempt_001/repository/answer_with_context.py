import os
import google.generativeai as genai

def answer_with_context(question: str, context: str) -> str:
    """
    Calls Google's Generative AI to answer a question using provided context.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""Answer the following question based on the provided context.

    Context: {context}
    Question: {question}

    Answer:"""
    response = model.generate_content(prompt)
    return response.text

