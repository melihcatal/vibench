
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

def summarize_document_records(documents: list[dict]) -> str:
    """
    Summarizes a list of document records using Google's Generative AI.

    Args:
        documents: A list of dictionaries, where each dictionary represents a document record.
                   It's assumed that each document has a 'content' field or similar
                   that contains text to be summarized.

    Returns:
        A string containing the summary of the document records.
    """
    aiplatform.init(project="your-gcp-project-id", location="us-central1")
    model = GenerativeModel("gemini-pro")

    combined_text = ""
    for doc in documents:
        # Assuming documents have a 'text_content' field for summarization
        if "text_content" in doc:
            combined_text += doc["text_content"] + "\n\n"
        elif "content" in doc:
            combined_text += doc["content"] + "\n\n"

    if not combined_text:
        return "No content found in documents to summarize."

    prompt = f"Please summarize the following document records:

{combined_text}"
    response = model.generate_content(prompt)

    return response.text
