import os
from google.cloud import aiplatform

def summarize_moderation_decisions(moderation_results, project_id=None, location=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")
    location = location or os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("GCP_PROJECT_ID not found in config or environment variables.")

    aiplatform.init(project=project_id, location=location)

    # Using a text-bison model for summarization
    # The model name should be specific, e.g., 'text-bison@001' or similar depending on availability.
    # For this example, I'll use a generic 'text-bison' assuming it maps to a default version.
    try:
        # Attempt to use a specific version first, then fallback to a general one
        model = aiplatform.Endpoint.from_pretrained("projects/{}/locations/{}/models/text-bison@001".format(project_id, location))
    except Exception:
        model = aiplatform.Endpoint.from_pretrained("text-bison")

    prompt = "Summarize the following moderation decisions:\n\n"
    for result in moderation_results:
        prompt += f"Text: {result.get('text', 'N/A')}, Toxicity: {result.get('toxicity', 'N/A')}, Decision: {result.get('decision', 'N/A')}\n"

    response = model.predict(prompt=prompt)
    return response.predictions[0].display_name
