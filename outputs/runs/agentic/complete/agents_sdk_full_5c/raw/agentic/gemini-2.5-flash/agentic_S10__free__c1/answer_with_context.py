import os
import google.generativeai as genai
from model_client import get_gemini_model

def answer_with_context(question: str, context: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM to answer a question using provided context.
    """
    model = get_gemini_model(model_name)
    prompt = f"""Answer the following question based *only* on the provided context.
    If the answer cannot be found in the context, respond with "I cannot answer based on the provided information."

    Context: {context}

    Question: {question}

    Answer:"""
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == '__main__':
    # Example usage - not for grading
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # context = "The capital of France is Paris. Paris is known for the Eiffel Tower."
    # question = "What is the capital of France?"
    # answer = answer_with_context(question, context)
    # print(answer)
    pass
