import os
from typing import List, Dict, Any
from openai import AzureOpenAI
from observability_models import LogQueryResult, IncidentSummaryRequest, IncidentSummaryResponse

def summarize_incident_logs(request: IncidentSummaryRequest, config: Dict[str, Any] = None) -> IncidentSummaryResponse:
    config = config or {}

    azure_openai_endpoint = config.get('AZURE_OPENAI_ENDPOINT', os.environ.get('AZURE_OPENAI_ENDPOINT'))
    azure_openai_key = config.get('AZURE_OPENAI_KEY', os.environ.get('AZURE_OPENAI_KEY'))
    azure_openai_deployment_name = config.get('AZURE_OPENAI_DEPLOYMENT_NAME', os.environ.get('AZURE_OPENAI_DEPLOYMENT_NAME'))

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_deployment_name]):
        raise ValueError("Azure OpenAI endpoint, key, or deployment name not configured.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01"
    )

    log_messages = [f"[{log.timestamp.isoformat()}] [{log.severity}] {log.message}" for log in request.log_entries]
    full_log_text = "\n".join(log_messages)

    prompt = f"""
    Summarize the following error logs to identify the core issue, potential impact, and possible root causes. 
    Focus on key events, recurring patterns, and critical information. 
    Logs:
    {full_log_text}
    """

    response = client.chat.completions.create(
        model=azure_openai_deployment_name, # This is the deployment name you chose when you deployed the model.
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes incident logs succinctly."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    summary = response.choices[0].message.content
    return IncidentSummaryResponse(summary=summary)
