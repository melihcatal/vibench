import os
from google.cloud import aiplatform

def check_safety_thresholds(text: str) -> bool:
    """
    Applies safety thresholds to decide whether to allow text using Google Cloud's Generative AI.
    """
    # Initialize the AI Platform client
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using other methods supported by google-cloud-sdk
    aiplatform.init(project=os.environ.get("GCP_PROJECT_ID"), location=os.environ.get("GCP_REGION"))

    # For text moderation, you might typically use a generative model and parse its safety attributes.
    # As of recent updates, direct programmatic access to fine-grained safety settings
    # for *specific thresholds* beyond the model's default response can be complex
    # and often involves interpreting the safety attributes returned by a model call.

    # This example demonstrates how to call a generative model (like 'gemini-pro')
    # and interpret its safety attributes.
    # The actual "thresholds" are often implicitly handled by the model's
    # safety filters, which can be configured at the project/model level
    # in Google Cloud AI Platform.
    # For a direct "apply category thresholds" requirement, one would typically
    # get scores from the model and then apply custom logic.

    # Using a generic text model for demonstration. Replace with an appropriate model if needed.
    model_name = "gemini-pro"
    
    try:
        model = aiplatform.preview.generative_models.GenerativeModel(model_name)
        response = model.generate_content(text,
                                        safety_settings={
                                            aiplatform.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: aiplatform.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                            aiplatform.HarmCategory.HARM_CATEGORY_HATE_SPEECH: aiplatform.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                            aiplatform.HarmCategory.HARM_CATEGORY_HARASSMENT: aiplatform.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                            aiplatform.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: aiplatform.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                                        }
                                       )
        # If the model blocks the content, an exception is usually raised or
        # the response will indicate a block reason in candidate.safety_ratings
        # if the request was not blocked outright but only flagged.
        # For simplicity, if we get here and no exception, it's generally allowed.
        # A more robust implementation would inspect response.candidates[0].safety_ratings
        # and compare with custom thresholds if the model returns scores instead of just blocking.

        if response.candidates:
            for safety_rating in response.candidates[0].safety_ratings:
                # Assuming THRESHOLD_UNSPECIFIED or HARM_BLOCK_THRESHOLD_UNSPECIFIED
                # means it's not blocked by this specific category or it falls below
                # the blocking threshold set in the request.
                # BLOCK_NONE means it was allowed.
                # A more detailed thresholding would parse probability and custom scores.
                if safety_rating.blocked:
                    print(f"Text blocked due to {safety_rating.category.name} at probability {safety_rating.probability.name}")
                    return False
            return True
        else:
            print("No candidates returned, potentially blocked by safety filters.")
            return False

    except Exception as e:
        print(f"An error occurred or text was blocked by safety settings: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    # Set your GCP project ID and region as environment variables or replace directly
    # os.environ["GCP_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["GCP_REGION"] = "us-central1"

    text_to_check_1 = "Hello, world!"
    if check_safety_thresholds(text_to_check_1):
        print(f"'{text_to_check_1}' is allowed.")
    else:
        print(f"'{text_to_check_1}' is not allowed.")

    text_to_check_2 = "I will kill you" # Example of text that might be blocked
    if check_safety_thresholds(text_to_check_2):
        print(f"'{text_to_check_2}' is allowed.")
    else:
        print(f"'{text_to_check_2}' is not allowed.")
