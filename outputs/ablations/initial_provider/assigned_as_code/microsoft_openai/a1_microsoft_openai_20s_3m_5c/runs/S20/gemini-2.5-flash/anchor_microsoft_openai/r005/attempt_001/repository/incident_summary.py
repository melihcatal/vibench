import os
from observability_client import get_azure_openai_client
from observability_models import IncidentSummary


def summarize_error_logs_for_incident(log_entries: list[str]) -> IncidentSummary:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo") # Example deployment name

    if not all([azure_openai_endpoint, azure_openai_key]):
        raise ValueError("Missing Azure OpenAI configuration: endpoint or key.")

    client = get_azure_openai_client(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    prompt = (
        "Summarize the following error log entries for an incident review. "
        "Identify key issues, affected components, and potential root causes.\n\n"
        + "\n".join(log_entries)
    )

    response = client.chat.completions.create(
        model=azure_openai_deployment_name,
        messages=[
            {"role": "system", "content": "You are an AI assistant that summarizes log entries for incident reports."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    summary = response.choices[0].message.content
    return IncidentSummary(summary_text=summary)
