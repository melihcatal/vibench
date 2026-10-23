import google.genai
from model_client import get_model_client

def answer_with_context(context, question, temperature=0.2, max_tokens=500):
    """Provides an answer to a question using provided context with Gemini API.

    Args:
        context (str): Background text for the model.
        question (str): The question to answer.
        temperature (float): Sampling temperature.
        max_tokens (int): Maximum tokens for the answer.

    Returns:
        str: Answer to the question.
    """
    client = get_model_client("gemini")
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:")
    response = client.generate_content(
        prompt,
        generation_params={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
            "response_mime_type": "text/plain",
        },
    )
    return response.text.strip()