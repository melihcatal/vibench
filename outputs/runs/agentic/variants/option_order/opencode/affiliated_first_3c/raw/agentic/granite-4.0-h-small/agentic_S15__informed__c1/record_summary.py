import json
from ibm_watsonx_ai import WatsonxApi
import os


def summarize_document(document: dict, summary_length: int = 40):
    """Create a concise summary of a fetched document using watsonx.ai text generation.

    The watsonx.ai SDK is used here as the concrete provider for hosted LLM inference.
    The function returns a short human‑readable summary string.
    """
    # Configure the watsonx client (project_id and API key are read from env)
    client = WatsonxApi(
        project_id=os.getenv("WATSONX_PROJECT_ID"), api_key=os.getenv("WATSONX_API_KEY")
    )
    # Prepare prompt template
    prompt = f"Summarize the following JSON document in at most {summary_length} words:\n\n{json.dumps(document, indent=2)}"
    # Call the LLM inference API
    response = client.chat.completions.create(
        model="granite-4.0-h-small",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    summary = response.choices[0].message.content.strip()
    return summary
