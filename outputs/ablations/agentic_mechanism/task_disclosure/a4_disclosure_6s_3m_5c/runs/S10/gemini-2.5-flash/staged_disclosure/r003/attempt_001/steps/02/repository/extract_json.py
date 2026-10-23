
import vertexai
from vertexai.generative_models import GenerativeModel, Part, GenerationConfig
import json
import os

def extract_json_from_text(text_content: str) -> dict:
    """
    Extracts structured JSON from the given text content using Google Vertex AI's Gemini-Pro model.
    """
    # Initialize Vertex AI
    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are set in your environment
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1 if not set

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    vertexai.init(project=project_id, location=location)

    # Load the model
    model = GenerativeModel("gemini-pro")

    # Define the prompt for JSON extraction
    prompt = f"""
    You are an expert at extracting structured JSON from text.
    Extract the relevant information from the following text and return it as a JSON object.
    If a field is not present, omit it from the JSON.

    Text:
    """
    {text_content}
    """

    Please provide the output in a JSON format.
    """

    # Set up generation config for JSON output
    generation_config = GenerationConfig(
        temperature=0.1,
        top_p=0.1,
        top_k=1,
        response_mime_type="application/json" # Explicitly request JSON output
    )

    try:
        response = model.generate_content(
            [prompt],
            generation_config=generation_config
        )
        # Assuming the model returns valid JSON directly in text attribute
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from model response: {e}")
        print(f"Model response: {response.text}")
        return {}
    except Exception as e:
        print(f"An error occurred during content generation: {e}")
        return {}

if __name__ == "__main__":
    # Example Usage:
    sample_text = """
    Customer name: John Doe, Order ID: 12345, Item: Laptop, Quantity: 1, Price: 1200.00 USD.
    Shipping Address: 123 Main St, Anytown, CA 90210.
    """
    extracted_data = extract_json_from_text(sample_text)
    print(json.dumps(extracted_data, indent=2))

    sample_text_2 = """
    Today's meeting discussed project Alpha. Key attendees were Alice and Bob.
    The next steps involve task A due by Friday and task B starting next Monday.
    No specific budget was mentioned.
    """
    extracted_data_2 = extract_json_from_text(sample_text_2)
    print(json.dumps(extracted_data_2, indent=2))
