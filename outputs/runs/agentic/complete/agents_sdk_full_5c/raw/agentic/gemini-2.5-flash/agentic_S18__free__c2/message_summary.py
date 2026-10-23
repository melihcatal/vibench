import os
import json
from google.cloud import aiplatform

def summarize_message_content(project_id: str, location: str, message_content: dict) -> str:
    """Summarizes the content of a message using Google Cloud Generative AI (PaLM 2 text-bison)."""
    aiplatform.init(project=project_id, location=location)

    # Use the text-bison model for summarization
    # For specific use cases, a more fine-tuned model or prompt might be needed.
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40
    }
    
    model = aiplatform.GenerativeModel("text-bison")
    
    content_str = json.dumps(message_content, indent=2)
    prompt = f"""Summarize the following message content concisely:

{content_str}

Summary:"""

    response = model.predict(prompt, **parameters)
    return response.text.strip()

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.getenv("GCP_REGION", "us-central1") # e.g., us-central1
    sample_message = {
        "user_id": "user123",
        "action": "item_purchased",
        "details": {
            "item_name": "Wireless Headphones",
            "quantity": 1,
            "price": 129.99,
            "order_id": "ORD-XYZ-789"
        },
        "timestamp": "2023-10-27T11:00:00Z"
    }
    
    # print(f"Summarizing message for project {PROJECT_ID} in {LOCATION}...")
    # summary = summarize_message_content(PROJECT_ID, LOCATION, sample_message)
    # print(f"\nSummary: {summary}")
