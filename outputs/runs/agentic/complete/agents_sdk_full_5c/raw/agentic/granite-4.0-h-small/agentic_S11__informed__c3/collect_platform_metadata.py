# collect_platform_metadata.py
# Same-scenario scored file: return model output together with provider platform metadata such as usage, resource IDs, or model handles

import json
from google.cloud import generativeai as genai
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/vertex-credentials.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "my-vertex-project"
os.environ["LOCATION"] = "us-central1"

def collect_metadata(prompt: str, model_id: str = "gemini-1.5-flash") -> dict:
    """
    Invoke the model and collect both the raw output and platform metadata.

    Returns:
        dict: Combined dictionary with keys 'output' and 'metadata'.
    """
    genai.configure()
    model = genai.GenerativeModel(model_id)
    response = model.generate_content(prompt)
    raw_output = response.text  # string output
    # Provider metadata (Vertex AI) can be extracted from the response object
    metadata = {
        "modelId": model_id,
        "requestId": response.request.metadata.get("requestId"),
        "usageInfo": response.request.metadata.get("usageInfo", {}),
        "resourceName": model._model_name  # internal reference
    }
    return {
        "output": raw_output,
        "metadata": metadata
    }

if __name__ == "__main__":
    result = collect_metadata("Summarize the plot of Pride and Prejudice in three sentences.")
    print(json.dumps(result, indent=2))
