
import google.cloud.aiplatform as aiplatform
from google.oauth2 import service_account
import os

# Set your Google Cloud project ID and location
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

# Initialize Vertex AI
aiplatform.init(project=PROJECT_ID, location=LOCATION)

def stream_model_generation(prompt: str, model_name: str = "gemini-pro"):
    """
    Streams output from a managed model platform (Google Vertex AI)
    while preserving provider response objects.
    """
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    # Load the generative model
    model = aiplatform.preview.generative_models.GenerativeModel(model_name)

    print(f"Sending prompt to {model_name}: {prompt}\n")

    # Start streaming generation
    responses = model.generate_content(
        contents=[prompt],
        stream=True
    )

    full_response_content = ""
    for response in responses:
        # Each 'response' is a provider-specific object (google.cloud.aiplatform_v1beta1.types.GenerateContentResponse)
        # You can access its attributes, e.g., 'candidates', 'usage_metadata'
        
        # Access the text part of the response
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            text_part = response.candidates[0].content.parts[0].text
            print(text_part, end="", flush=True)
            full_response_content += text_part
        
        # You can also inspect the full response object for more details
        # For demonstration, let's print a part of the raw response object
        # print(f"\nRaw response object type: {type(response)}")
        # print(f"Safety ratings: {response.candidates[0].safety_ratings if response.candidates else 'N/A'}\n")

    print("\n\n--- End of Stream ---")
    return full_response_content

if __name__ == "__main__":
    test_prompt = "Tell me a short story about a brave knight and a wise dragon."
    stream_model_generation(test_prompt)
