import os
from openai import AzureOpenAI
from observability_models import SummarizationRequest

def incident_summary(request: SummarizationRequest) -> dict:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_deployment_name]):
        raise ValueError("Missing Azure OpenAI environment variables: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_NAME")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-01", # Or your specific API version
    )

    log_content = "\n".join(request.log_entries)
    prompt = f"""Summarize the following error logs for an incident review:

{log_content}

Summary:"""

    response = client.chat.completions.create(
        model=azure_openai_deployment_name, # deployment name
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes incident logs."}, # Use system message for context
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    
    summary = response.choices[0].message.content
    return {"summary": summary}
