import os
import google.generativeai as genai
from model_client import get_gemini_model

def answer_with_context(question: str, context: str, model_name: str = "gemini-pro") -> str:
    """
    Calls Google Gemini API to answer a question using provided context.
    """
    model = get_gemini_model(model_name)
    prompt = f"Using the following context, answer the question. If the answer is not in the context, say so.\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"
    response = model.generate_content(prompt)
    return response.text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY env var)
    # sample_context = "The capital of France is Paris. It is known for the Eiffel Tower."
    # sample_question = "What is the capital of France?"
    # print(answer_with_context(sample_question, sample_context))
    pass
