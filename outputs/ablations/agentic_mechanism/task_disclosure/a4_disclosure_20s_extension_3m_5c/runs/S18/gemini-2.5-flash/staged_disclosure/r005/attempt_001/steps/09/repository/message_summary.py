from google.cloud import aiplatform

def summarize_message_results(results: dict) -> str:
    """
    Summarizes message processing results using Google Cloud Vertex AI.

    Args:
        results: A dictionary containing the message processing results.

    Returns:
        A string summary of the results.
    """
    aiplatform.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    prompt = f"""Please summarize the following message processing results:
{results}
"""
    response = model.generate_content(prompt)
    return response.text.strip()

