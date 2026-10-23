
from google.cloud import aiplatform
import json

def extract_json_from_text(project_id: str, location: str, text: str) -> dict:
    """
    Calls a hosted LLM (Vertex AI Gemini Pro) to extract structured JSON from text.

    Args:
        project_id: Your Google Cloud project ID.
        location: The region where your Vertex AI models are hosted (e.g., "us-central1").
        text: The input text from which to extract JSON.

    Returns:
        A dictionary representing the extracted JSON.
    """
    aiplatform.init(project=project_id, location=location)

    # Use the concrete model identifier for Gemini Pro
    model = aiplatform.preview.language_models.ChatModel.from_pretrained("gemini-pro")

    prompt = f"""
    Extract any structured JSON object from the following text. If no JSON is present, return an empty JSON object {{}}.
    Do not include any text apart from the JSON.

    Text:
    {text}

    JSON:
    """

    response = model.predict(prompt)
    try:
        # Assuming the model directly returns JSON as text
        extracted_json = json.loads(response.text.strip())
        return extracted_json
    except json.JSONDecodeError:
        print("Warning: Model did not return valid JSON. Returning empty dict.")
        return {}

if __name__ == "__main__":
    # Replace with your Google Cloud project ID and desired location
    your_project_id = "your-gcp-project-id"
    your_location = "us-central1"

    example_text_with_json = """
    Here is some random text, and embedded within it is a JSON object:
    ```json
    {
      "name": "John Doe",
      "age": 30,
      "isStudent": false,
      "courses": ["History", "Math"]
    }
    ```
    More text follows.
    """

    example_text_without_json = """
    This is just plain text without any JSON structure inside.
    """

    print("Extracting JSON from text with embedded JSON:")
    result_with_json = extract_json_from_text(your_project_id, your_location, example_text_with_json)
    print(json.dumps(result_with_json, indent=2))

    print("\nExtracting JSON from text without JSON:")
    result_without_json = extract_json_from_text(your_project_id, your_location, example_text_without_json)
    print(json.dumps(result_without_json, indent=2))
