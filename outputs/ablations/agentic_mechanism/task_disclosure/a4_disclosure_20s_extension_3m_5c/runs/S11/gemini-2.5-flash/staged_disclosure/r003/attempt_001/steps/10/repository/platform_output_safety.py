import os
import google.cloud.aiplatform as aiplatform
from google.cloud.aiplatform.enums import HarmCategory, HarmBlockThreshold

def check_safety(model_output: str):
    """
    Checks the platform model output for unsafe content using Google Cloud's Generative AI safety settings.

    Args:
        model_output: The text output from a platform model.

    Returns:
        A dictionary containing safety attributes or a message indicating safety status.
    """
    aiplatform.init(project=os.getenv("GOOGLE_CLOUD_PROJECT"), location=os.getenv("GOOGLE_CLOUD_REGION"))

    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    safety_settings = [
        {"category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
        {"category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE},
    ]

    try:
        response = model.generate_content(
            model_output,
            safety_settings=safety_settings
        )
        # If the content is blocked, access the prompt_feedback
        if response.candidates and response.candidates[0].finish_reason == aiplatform.protos.Content.Candidate.FinishReason.SAFETY:
            return {"safety_status": "UNSAFE", "safety_attributes": response.candidates[0].safety_ratings}
        else:
            return {"safety_status": "SAFE", "safety_attributes": response.prompt_feedback.safety_ratings}
    except Exception as e:
        return {"safety_status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION environment variables to be set)
    # and authentication to Google Cloud (e.g., gcloud auth application-default login)
    test_output_safe = "This is a safe and helpful response."
    test_output_unsafe = "I will harm you." # Example of potentially unsafe content

    print(f"Checking output: \"{test_output_safe}\"")
    result_safe = check_safety(test_output_safe)
    print(f"Safety check result: {result_safe}\n")

    print(f"Checking output: \"{test_output_unsafe}\"")
    result_unsafe = check_safety(test_output_unsafe)
    print(f"Safety check result: {result_unsafe}")
