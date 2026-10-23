import google.generativeai as genai
import os

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM (Google Gemini Pro) to answer a question using provided context.

    Args:
        question: The question to ask the LLM.
        context: The context to provide to the LLM for answering the question.

    Returns:
        The LLM's answer.
    """
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-pro')

    # Construct the prompt for the LLM
    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer the question truthfully based on the provided context. If the answer is not available in the context, state that you don't have enough information.
    """

    # Generate content using the model
    response = model.generate_content(prompt)

    # Return the text from the response
    return response.text.strip()

