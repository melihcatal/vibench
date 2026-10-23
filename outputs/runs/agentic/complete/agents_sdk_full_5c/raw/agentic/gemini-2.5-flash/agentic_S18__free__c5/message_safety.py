import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image, HarmCategory, HarmBlockThreshold

def check_message_safety(project_id: str, location: str, message_payload_text: str) -> dict:
    """Checks message payload text for unsafe content using Google Cloud Generative AI (Gemini Pro) safety features."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    # The safety settings are applied during content generation. If the input itself is unsafe,
    # the API might block the request or flag it in the response.
    # For checking input safety, we can attempt a generation with strict safety settings
    # or analyze the response safety attributes.

    # A simple way to check is to ask the model to process/analyze the content
    # and then inspect the safety attributes of the response.

    # For a direct safety check of input without generating new content,
    # one typically relies on pre-analysis or specific APIs. However, if the intent
    # is to see if the content would be blocked or flagged by a LLM, a simple prompt suffices.
    # We'll use a prompt that encourages the model to evaluate the text.
    prompt = f"""Review the following text for any unsafe content related to hate speech, sexual content, harmful content, or dangerous acts. 
    Indicate if it contains any such content and provide a brief assessment. If no unsafe content is found, state that it is safe.

    Text: \'''{message_payload_text}\'''

    Assessment:"""

    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
    )

    safety_attributes = {
        "text_content": message_payload_text,
        "blocked": False,
        "block_reason": None,
        "safety_ratings": []
    }

    if not response._raw_response.candidates:
        safety_attributes["blocked"] = True
        safety_attributes["block_reason"] = "No candidate generated, possibly due to safety settings."
    else:
        for rating in response._raw_response.candidates[0].safety_ratings:
            safety_attributes["safety_ratings"].append({
                "category": rating.category.name,
                "probability": rating.probability.name,
                "blocked": rating.blocked
            })
        safety_attributes["model_assessment"] = response.text.strip()

    print(f"Safety check results: {safety_attributes}")
    return safety_attributes

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    LOCATION = "us-central1" # Or your preferred Vertex AI region

    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        safe_text = "This is a perfectly normal message about a product update."
        unsafe_text = "I will harm you and your family!"

        print("\n--- Checking safe text ---")
        check_message_safety(PROJECT_ID, LOCATION, safe_text)

        print("\n--- Checking unsafe text ---")
        check_message_safety(PROJECT_ID, LOCATION, unsafe_text)
