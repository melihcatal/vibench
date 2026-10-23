import os
from google.cloud import aiplatform
from typing import List, Dict, Any

def summarize_embedding_job_results(job_results: List[Dict[str, Any]], project_id: str, location: str) -> str:
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name="gemini-pro")
    
    results_text = "\n".join([str(result) for result in job_results])
    
    prompt = f"Summarize the following embedding job results:\n\n{results_text}\n\nSummary:"
    response = model.generate_content(prompt)
    return response.text