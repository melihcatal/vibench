import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ResponseBlockedError
from typing import Dict, Any, Tuple

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

def collect_platform_metadata(prompt: str) -> Tuple[str, Dict[str, Any]]:
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    model = GenerativeModel("gemini-pro")
    
    try:
        response = model.generate_content(prompt)
        output_text = response.text
        
        metadata = {
            "usage_metadata": {
                "prompt_token_count": response.usage_metadata.prompt_token_count,
                "candidates_token_count": response.usage_metadata.candidates_token_count,
                "total_token_count": response.usage_metadata.total_token_count,
            }
        }
        return output_text, metadata
    except ResponseBlockedError as e:
        return "", {"error": "Response blocked due to safety concerns", "details": str(e)}
