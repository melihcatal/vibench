import os
from typing import Dict, Any
from google.cloud import aiplatform


def record_summary(document_data: Dict[str, Any], project_id: str = None, location: str = "us-central1") -> str:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud Project ID not provided and not found in GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    # Assuming the document_data has a 'text_content' field to summarize
    text_to_summarize = document_data.get("text_content", "")
    if not text_to_summarize:
        return "No text content found for summarization."

    # Using a pre-trained text-bison model for summarization
    # For a production application, you might fine-tune a model or use a more specific prompt
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 200,
        "top_p": 0.95,
        "top_k": 40,
    }
    model = aiplatform.predict.PredictionClient.from_instance("text-bison")
    prompt = f"Summarize the following text:\n{text_to_summarize}\nSummary:"
    
    response = model.predict(instances=[{"prompt": prompt}], parameters=parameters)
    
    # The response structure might vary; adjust based on actual Vertex AI output
    # Assuming the summary is in the 'predictions' field of the first instance
    if response.predictions:
        return response.predictions[0]
    return "Could not generate summary."
