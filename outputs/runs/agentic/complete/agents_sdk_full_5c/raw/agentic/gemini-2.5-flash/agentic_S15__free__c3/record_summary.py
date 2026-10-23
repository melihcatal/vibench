from typing import Dict, Any, List, Optional
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content, Image

def summarize_records(records: List[Dict[str, Any]], project_id: str, location: str = "us-central1") -> Optional[str]:
    """Summarizes a list of document records using a Google Cloud Generative AI model.

    Args:
        records (List[Dict[str, Any]]): A list of dictionaries, where each dictionary is a document record.
        project_id (str): Your Google Cloud project ID.
        location (str): The Google Cloud region for Vertex AI.

    Returns:
        Optional[str]: A summary of the records, or None if summarization fails.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for text summarization

    if not records:
        return "No records to summarize."

    # Convert records to a more readable string format for the model
    records_text = "Records to summarize:\n"
    for i, record in enumerate(records):
        records_text += f"\nRecord {i+1}:\n"
        for key, value in record.items():
            records_text += f"  {key}: {value}\n"

    prompt = f"Please provide a concise summary of the following document records. Focus on key information and common themes:\n\n{records_text}"

    try:
        # Using generate_content for a simple text-to-text summary
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            summary = "".join([part.text for part in response.candidates[0].content.parts])
            print("Records summarized successfully using Gemini Pro.")
            return summary
        else:
            print("Gemini Pro did not return a valid summary.")
            return None
    except Exception as e:
        print(f"Error summarizing records with Gemini Pro: {e}")
        return None

if __name__ == "__main__":
    # Example Usage:
    # Replace 'your-gcp-project-id' with your actual Google Cloud Project ID
    # Ensure you have enabled the Vertex AI API and have appropriate permissions.
    # For local execution, ensure gcloud is authenticated or GOOGLE_APPLICATION_CREDENTIALS is set.
    GCP_PROJECT_ID = "your-gcp-project-id" # <<< IMPORTANT: Update this to your GCP Project ID

    sample_records = [
        {
            "id": "prod001",
            "name": "Laptop Pro",
            "category": "Electronics",
            "price": 1200.00,
            "description": "High performance laptop for professionals."
        },
        {
            "id": "prod002",
            "name": "Gaming Mouse",
            "category": "Electronics",
            "price": 75.00,
            "description": "Ergonomic gaming mouse with customizable RGB."
        },
        {
            "id": "user001",
            "username": "johndoe",
            "email": "john.doe@example.com",
            "role": "customer",
            "last_login": "2023-10-26T10:00:00Z"
        },
        {
            "id": "prod003",
            "name": "Smartwatch X",
            "category": "Wearables",
            "price": 250.00,
            "description": "Advanced smartwatch with health tracking."
        }
    ]

    print("\nAttempting to summarize sample records...")
    try:
        summary = summarize_records(sample_records, GCP_PROJECT_ID)
        if summary:
            print("\n--- Summary ---")
            print(summary)
            print("-----------------")
        else:
            print("Failed to generate summary.")
    except Exception as e:
        print(f"Example usage failed: {e}")
