# [LATER-STEP] quality_summary.py

import json
from ibm_watsonx_ai.services import GraniteChatModel
from ibm_watsonx_ai import APIClient


def summarize_quality_issues(translations):
    """Summarize translation quality issues using IBM Granite model.

    Args:
        translations (list[dict]): List of dicts returned from translation functions.
            Each dict should contain 'translated_text' and optionally other metadata.

    Returns:
        dict: A structured summary of detected issues (e.g., mistranslations, placeholders).
    """
    # Initialize Watsonx client using environment variables WATSONX_API_KEY and WATSONX_PROJECT_ID
    api_client = APIClient()
    model = GraniteChatModel(api_client=api_client, model_id="granite-3-8b-instruct")

    # Combine translated texts for analysis
    texts = [t["translated_text"] for t in translations]
    batch = "\n---\n".join(texts)

    # Create a prompt for the model to assess
    prompt = f"You are a quality assurance reviewer. Analyze the following translated texts and produce a concise JSON summary of any issues. List each issue type and give a short example.\n\nTranslated texts:\n{batch}"

    # Call the model (using the same-scenario provider for later-step)
    response = model.chat(messages=[{"role": "user", "content": prompt}])
    # Assume the model returns a JSON string
    issues = json.loads(response.content)
    return issues
