import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def summarize_records(project_id: str, location: str, records: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of document records using Google Cloud Vertex AI (text-bison model).

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        records: A list of document records to summarize.

    Returns:
        A string containing the summary of the records.
    """
    aiplatform.init(project=project_id, location=location)
    # Using the text-bison model for summarization
    # https://cloud.google.com/vertex-ai/docs/generative/model-reference/text#text-bison
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "top_p": 0.95,
        "top_k": 40
    }
    model = aiplatform.GenerativeModel("text-bison")

    # Prepare the prompt for summarization
    record_texts = []
    for i, record in enumerate(records):
        record_texts.append(f"Document {i+1}: {record}")
    
    prompt = "Please summarize the following documents:\n\n" + "\n".join(record_texts) + "\n\nSummary:"

    response = model.predict(prompt, **parameters)
    return response.text
