from vertexai.preview.generative_models import GenerativeModel
import os


def record_summary(document_content: dict) -> str:
    model = GenerativeModel("gemini-pro")
    text_to_summarize = str(document_content) # Convert dict to string for summarization
    
    response = model.generate_content(
        f"Summarize the following document content:

{text_to_summarize}"
    )
    
    return response.text
