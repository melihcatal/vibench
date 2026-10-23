import os
from typing import List
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference


def check_corpus_safety(texts: List[str]) -> List[Dict[str, str]]:
    """Check corpus texts for harmful content using WatsonX.ai HAP detection."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    
    credentials = Credentials(api_key)
    model_inference = ModelInference(
        model_id="ibm/hap-detection",
        credentials=credentials,
        project_id=project_id
    )
    
    results = []
    for text in texts:
        response = model_inference.generate_text(prompt=text)
        is_flagged = "flagged" in response.lower()
        results.append({
            "text": text,
            "is_safe": not is_flagged,
            "details": response
        })
    
    return results