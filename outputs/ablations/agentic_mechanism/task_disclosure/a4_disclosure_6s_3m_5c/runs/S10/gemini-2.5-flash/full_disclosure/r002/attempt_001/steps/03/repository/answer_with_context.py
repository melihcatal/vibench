import google.generativeai as genai
import os

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM to answer a question using provided context.

    Args:
        question: The question to be answered.
        context: The context to use for answering the question.

    Returns:
        The answer from the LLM.
    """
    # Configure the API key (replace with your actual API key or environment variable)
    # It is recommended to set GOOGLE_API_KEY as an environment variable
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Use a specific model, e.g., 'gemini-pro'
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Using the following context, answer the question:

Context: {context}

Question: {question}

Answer:"

    response = model.generate_content(prompt)

    return response.text
