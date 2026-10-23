import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, FinishReason
import json

def extract_json_from_text(text: str, prompt: str) -> dict:
    """
    Calls a hosted LLM (Vertex AI's Gemini Pro) to extract structured JSON from text.

    Args:
        text: The input text from which to extract JSON.
        prompt: The prompt to guide the LLM in extracting JSON.

    Returns:
        A dictionary representing the extracted JSON.
    """
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION") # Replace with your Google Cloud project ID and region
    model = GenerativeModel("gemini-pro")

    full_prompt = f"{prompt}\n\nText: {text}\n\nExtract the structured JSON from the text above."

    response = model.generate_content(full_prompt)

    try:
        # Assuming the LLM returns JSON directly in its text response
        extracted_json = json.loads(response.text)
        return extracted_json
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from LLM response.")
        return {}

if __name__ == '__main__':
    # Example Usage:
    sample_text = "The user's name is John Doe and he is 30 years old. His email is john.doe@example.com."
    json_prompt = "Extract the user's name, age, and email into a JSON object."

    extracted_data = extract_json_from_text(sample_text, json_prompt)
    print(extracted_data)

    sample_text_2 = "Product: Laptop, Price: 1200, Currency: USD. Customer rating: 4.5 stars."
    json_prompt_2 = "Extract the product name, price, currency, and rating into a JSON object."

    extracted_data_2 = extract_json_from_text(sample_text_2, json_prompt_2)
    print(extracted_data_2)
