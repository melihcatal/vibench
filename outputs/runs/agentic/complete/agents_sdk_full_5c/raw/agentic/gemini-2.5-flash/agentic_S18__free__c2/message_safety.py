import os
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def check_message_safety(project_id: str, location: str, message_text: str) -> dict:
    """Checks message payload text for unsafe content using Google Cloud Generative AI (PaLM 2 text-bison).
    Returns a dictionary indicating safety attributes.
    """
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.GenerativeModel("text-bison")

    # Safety settings to block content that falls into certain categories
    # and thresholds. Adjust as needed for specific application requirements.
    safety_settings = [
        {
            "category": HarmCategory.HARM_CATEGORY_HARASSMENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        {
            "category": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            "threshold": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
    ]

    response = model.generate_content(
        contents=[message_text],
        safety_settings=safety_settings
    )

    # The response object contains safety_ratings if the content was evaluated.
    # If the content was blocked, response.prompt_feedback will contain the reason.
    safety_analysis = {
        "is_safe": True,
        "blocked_reason": None,
        "safety_ratings": []
    }

    if response.prompt_feedback and response.prompt_feedback.block_reason:
        safety_analysis["is_safe"] = False
        safety_analysis["blocked_reason"] = str(response.prompt_feedback.block_reason)
    
    if hasattr(response, 'candidates') and response.candidates:
        # Assuming we are interested in the safety ratings of the input prompt itself
        # and not necessarily the (empty) generated content if it was blocked.
        # The prompt_feedback already gives us blocking info.
        # If we were generating content, we'd check candidate.safety_ratings.
        pass # We already handled prompt_feedback for blocking.

    # Note: Google Cloud Generative AI Client Library for Python does not expose
    # prompt safety ratings directly on the input if no content is generated. 
    # The block_reason on prompt_feedback is the primary signal for unsafe input.

    # For a more detailed breakdown of individual safety scores, one might need
    # to use the REST API or a dedicated moderation API if available.

    return safety_analysis

if __name__ == '__main__':
    # Example usage:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    LOCATION = os.getenv("GCP_REGION", "us-central1")

    safe_text = "This is a perfectly safe message about a product purchase."
    unsafe_text = "I will harm you and your family!"

    # print(f"Checking safety for project {PROJECT_ID} in {LOCATION}...")
    # print(f"\nChecking safe_text: \'{safe_text}\'")
    # safe_result = check_message_safety(PROJECT_ID, LOCATION, safe_text)
    # print(f"Safe Text Safety Analysis: {json.dumps(safe_result, indent=2)}")

    # print(f"\nChecking unsafe_text: \'{unsafe_text}\'")
    # unsafe_result = check_message_safety(PROJECT_ID, LOCATION, unsafe_text)
    # print(f"Unsafe Text Safety Analysis: {json.dumps(unsafe_result, indent=2)}")
