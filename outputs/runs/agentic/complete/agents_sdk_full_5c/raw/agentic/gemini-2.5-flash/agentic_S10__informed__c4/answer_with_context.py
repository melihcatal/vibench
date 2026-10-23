import google.generativeai as genai
import os
from model_client import get_gemini_client

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (Gemini) to answer a question using provided context.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    
    prompt = f"""Based on the following context, answer the question. If the answer is not in the context, state that you don't know.

Context:
{context}

Question: {question}

Answer:
"""
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == '__main__':
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual key or set it in your environment
    
    context_text = "The capital of France is Paris. Paris is also known as the 'City of Love'. The Eiffel Tower is a famous landmark in Paris."
    
    question_1 = "What is the capital of France?"
    answer_1 = answer_with_context(question_1, context_text)
    print(f"Context: {context_text}\nQuestion: {question_1}\nAnswer: {answer_1}\n")
    
    question_2 = "What is the highest mountain in the world?"
    answer_2 = answer_with_context(question_2, context_text)
    print(f"Context: {context_text}\nQuestion: {question_2}\nAnswer: {answer_2}")
