import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from typing import List, Dict

# TODO: Replace with your Google Cloud project ID and location
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def summarize_document_records(records: List[Dict]) -> List[Dict]:
    """
    Summarizes retrieved document records using Google Vertex AI's GenerativeModel.

    Args:
        records: A list of dictionaries, where each dictionary represents a document record.
                 Each record is expected to have a 'content' field containing the text to summarize.

    Returns:
        A list of dictionaries, where each original record is augmented with a 'summary' field.
    """
    model = GenerativeModel("gemini-pro")
    summarized_records = []

    for record in records:
        if "content" in record and isinstance(record["content"], str):
            prompt = f"Summarize the following document content:
{record["content"]}"
            response = model.generate_content(prompt)
            # Accessing text content directly from the 'text' attribute of the Part object
            summary = response.candidates[0].content.parts[0].text if response.candidates and response.candidates[0].content.parts else "No summary generated."
            record["summary"] = summary
        else:
            record["summary"] = "No content to summarize or content is not a string."
        summarized_records.append(record)

    return summarized_records

