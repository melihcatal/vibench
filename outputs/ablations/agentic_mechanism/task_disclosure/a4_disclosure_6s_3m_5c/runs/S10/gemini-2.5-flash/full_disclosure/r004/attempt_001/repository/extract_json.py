from google.cloud import aiplatform

def extract_json_from_text(text: str, project_id: str, location: str, model_id: str = "gemini-pro"):
    """
    Calls a hosted LLM (Google Cloud Vertex AI) to extract structured JSON from text.

    Args:
        text: The input text from which to extract JSON.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").
        model_id: The ID of the model to use (defaults to "gemini-pro").

    Returns:
        A dictionary representing the extracted JSON, or None if extraction fails.
    """
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_id)

    prompt = f"""Extract all structured JSON objects from the following text.
If no JSON is found, return an empty JSON object {{}}.

Text:
'''
{text}
'''

Extracted JSON:
"""
    try:
        response = model.generate_content(prompt)
        if response.candidates and response.candidates[0].content.parts:
            # Assuming the model returns valid JSON directly in the text
            json_str = response.candidates[0].content.parts[0].text.strip()
            import json
            return json.loads(json_str)
        return {}
    except Exception as e:
        print(f"Error extracting JSON: {e}")
        return {}

