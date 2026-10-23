import os
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_text_safety(project_id: str, location: str, text_content: str, model_name: str = "gemini-pro") -> dict:
    """
    Checks user-generated document fields for unsafe content using Google Cloud Vertex AI (Generative AI).
    """
    try:
        aiplatform.init(project=project_id, location=location)
        
        # Initialize the model
        model = aiplatform.preview.generative_models.GenerativeModel(model_name)
        
        # Perform content moderation (safety attributes are part of generate_content response)
        response = model.generate_content(
            text_content,
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }
        )
        
        # The actual safety attributes are usually in the candidates part of the response
        # If the content is blocked, an exception might be raised or no candidates returned.
        if not response.candidates:
            print("Content was blocked due to safety concerns.")
            return {"blocked": True, "reason": "Content blocked by safety settings"}
        
        # For detailed safety attributes, you might need to access specific fields
        # The exact structure depends on the model version and API.
        # This is a simplified check for blocked status.
        
        print("Text safety check completed.")
        return {"blocked": False, "safety_ratings": [c.safety_ratings for c in response.candidates] if response.candidates else []}

    except Exception as e:
        print(f"Error checking text safety: {e}")
        # A more robust implementation would parse specific error types for content blocking
        # For now, if an error occurs, we assume it might be related to safety blocking or API issue.
        return {"blocked": True, "reason": str(e)}

if __name__ == '__main__':
    # Example usage (requires Google Cloud project, enabled Vertex AI API, and authentication)
    # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/your/key.json' # Or gcloud auth login
    # project_id = "your-gcp-project-id" # Replace with your GCP project ID
    # location = "us-central1" # Replace with your Vertex AI region

    # safe_text = "This is a perfectly safe document content."
    # unsafe_text = "I will kill you all!"

    # if project_id and location:
    #     print("\nChecking safe text:")
    #     safe_result = check_text_safety(project_id, location, safe_text)
    #     print(f"Safe text result: {safe_result}")

    #     print("\nChecking unsafe text:")
    #     unsafe_result = check_text_safety(project_id, location, unsafe_text)
    #     print(f"Unsafe text result: {unsafe_result}")
    # else:
    #     print("Please set project_id and location variables for example usage.")
