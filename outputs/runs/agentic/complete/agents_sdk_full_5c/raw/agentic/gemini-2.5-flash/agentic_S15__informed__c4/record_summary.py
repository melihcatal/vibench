import os
import google.generativeai as genai
from typing import Dict, Any, List

def summarize_records(records: List[Dict[str, Any]], model_name: str = "gemini-pro") -> str:
    """
    Summarizes a list of document records using the Google Gemini API.
    Requires GOOGLE_API_KEY environment variable to be set.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)

    if not records:
        return "No records to summarize."

    # Combine relevant fields from records into a single string for summarization
    # This is a simplified approach; a more sophisticated one might involve selecting specific fields
    combined_text = "".join([f"Document ID: {record.get('document_id')}, Data: {record.get('data')}\n" for record in records])

    prompt = f"Please provide a concise summary of the following document records:\n\n{combined_text}"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing records: {e}"

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY to be set up)
    sample_records = [
        {"document_id": "doc1", "data": {"title": "Meeting Notes", "content": "Discussed Q3 results and action items."}},
        {"document_id": "doc2", "data": {"title": "Project Alpha Update", "content": "Progress on module A is good, module B delayed."}}
    ]
    summary = summarize_records(sample_records)
    print(f"Summary: {summary}")
