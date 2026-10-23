from google.cloud import aiplatform
from database_models import DocumentRecord
from typing import List
import os

def summarize_records(records: List[DocumentRecord]) -> str:
    # Initialize Vertex AI
    aiplatform.init(
        project=os.environ.get("GCP_PROJECT_ID"),
        location=os.environ.get("GCP_REGION")
    )

    # Use a generative model (e.g., Gemini)
    model = aiplatform.preview.language_models.ChatModel.from_pretrained("gemini-pro")

    context = "You are a helpful assistant that summarizes document records. Provide a concise summary of the key information from the following records."
    
    record_texts = [f"Document ID: {record.id}, Data: {record.data}" for record in records]
    prompt = "\n".join(record_texts)

    response = model.predict(prompt=prompt, context=context)
    return response.text
