import os
from google.cloud import aiplatform
from google.generativeai import GenerativeModel, configure

def answer_with_context(question: str, context: str) -> str:
    """
    Answers a question based on the provided context using a Google Generative AI model.
    """
    # Configure the Google Generative AI client
    # configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # For Vertex AI:
    # aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location=os.environ.get("GOOGLE_CLOUD_LOCATION"))
    # model = GenerativeModel(model_name="gemini-pro")

    # For Gemini API
    model = GenerativeModel(model_name="gemini-pro")

    prompt = f"Given the following context, answer the question. If the answer is not in the context, state that you don't know.

Context: {context}

Question: {question}

Answer:"
    response = model.generate_content(prompt)
    return response.text
