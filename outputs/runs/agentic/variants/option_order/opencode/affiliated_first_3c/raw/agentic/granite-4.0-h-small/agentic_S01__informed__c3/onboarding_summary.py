import os
from ibm_watsonx_ai import Client
from ibm_watsonx_ai.consts import EndpointType

api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")

client = Client(api_key=api_key, project_id=project_id)
ubench_endpoint = client.service_instance_endpoint(endpoint_type=EndpointType.UBENCH)

SUMMARY_SYSTEM_PROMPT = (
    "You are a helpful assistant that generates concise summaries of onboarding notes."
)


def summarize_onboarding_state(note_ids):
    """Summarize a list of onboarding note IDs for support.
    Returns a concatenated summary string.
    """
    summaries = []
    for nid in note_ids:
        note_content = client.get_note_content(nid)  # placeholder API
        summary = summarize_text(note_content)
        summaries.append(f"Note {nid}: {summary}")
    return "\\n\\n".join(summaries)


def summarize_text(text):
    """Generate a short summary using the hosted LLM."""
    response = ubench_endpoint.completions.create(
        model="granite-3.2-instruct",
        prompt=SUMMARY_SYSTEM_PROMPT + "\\n\\n" + text,
        max_tokens=150,
    )
    return response["generated_text"].split("\\n")[0]
