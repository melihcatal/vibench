from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

def summarize_document(text_content: str) -> str:
    # Initialize Vertex AI
    aiplatform.init()

    model = GenerativeModel("gemini-pro") # Using Gemini Pro for summarization
    response = model.generate_content(f"Summarize the following document content:\n\n{text_content}")
    return response.text
