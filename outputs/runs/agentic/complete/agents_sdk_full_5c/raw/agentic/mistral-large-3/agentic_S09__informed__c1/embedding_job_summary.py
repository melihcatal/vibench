from typing import List, Dict, Any
from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials
import os


def summarize_embedding_job(job_results: List[Dict[str, Any]]) -> str:
    """Summarize embedding job results using IBM WatsonX.ai Granite model."""
    api_key = os.getenv("WATSONX_API_KEY")
    project_id = os.getenv("WATSONX_PROJECT_ID")
    
    credentials = Credentials(api_key)
    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        credentials=credentials,
        project_id=project_id
    )
    
    summary_prompt = (
        "Summarize the following embedding job results in a concise report:\n"
        f"{job_results}\n\n"
        "Include key metrics like total texts embedded, embedding dimensions, and any anomalies."
    )
    
    response = model.generate_text(prompt=summary_prompt)
    return response