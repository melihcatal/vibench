import os
from typing import List
from google.cloud import aiplatform

def incident_summary(error_logs: List[str], project_id: str, location: str = "us-central1") -> str:
    aiplatform.init(project=project_id, location=location)
    
    # Use a pre-trained model for text generation, e.g., text-bison
    # Make sure to enable the Vertex AI API and have the necessary permissions.
    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 1024,
        "top_p": 0.95,
        "top_k": 40
    }
    
    # For models supporting generate_content, use that method
    try:
        model = aiplatform.get_model_registry().get_latest_model("text-bison@001")
    except Exception as e:
        # Fallback for models without direct registry access or if name changes
        print(f"Warning: Could not get text-bison@001 from model registry. Trying with TextGenerationModel. Error: {e}")
        model = aiplatform.TextGenerationModel.from_pretrained("text-bison@001")

    log_content = "\n".join(error_logs)
    prompt = f"""Summarize the following error logs for an incident review. Highlight key issues, potential causes, and frequency. 

Logs:
{log_content}

Summary:"""

    response = model.predict(
        prompt,
        **parameters
    )

    return response.text
