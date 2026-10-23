import os
from google.cloud import aiplatform
from google.cloud.aiplatform.enums import HarmCategory, HarmBlockThreshold
from model_models import SafetyResult, SafetyRating
from typing import List

# Initialize Vertex AI for safety checks
# This client doesn't need to be part of model_client.py as it's a specific feature
# and the prediction client is for generation.
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

if not PROJECT_ID:
    raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

aiplatform.init(project=PROJECT_ID, location=LOCATION)


def check_content_safety(text: str, model_name: str = "gemini-pro") -> SafetyResult:
    """
    Checks prompts and generated text for unsafe content using Google Cloud Vertex AI's safety features.

    Note: For `gemini-pro`, safety settings are typically part of the `GenerativeModel` directly.
    The client-side safety evaluation is done when `generate_content` is called.
    This function specifically demonstrates retrieving safety attributes from a response.
    """
    model = aiplatform.GenerativeModel(model_name)

    # A simple generate call to get content and safety attributes
    # In a real scenario, you might integrate this with your actual generation call
    # For demonstration, we'll make a call that includes safety

    # Setting safety_settings here to illustrate how it's done for a generation call.
    # The response will contain safety_ratings regardless if they are set explicitly.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    try:
        response = model.generate_content(
            contents=text,
            safety_settings=safety_settings,  # Applying safety settings
        )

        # Check if the response was blocked by safety filters
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            safety_ratings = []
            for rating in response.prompt_feedback.safety_ratings:
                safety_ratings.append(
                    SafetyRating(
                        category=rating.category.name,
                        probability=rating.probability.name,
                    )
                )
            return SafetyResult(blocked=True, safety_ratings=safety_ratings)

        if response.candidates:
            candidate = response.candidates[0]
            if (
                candidate.finish_reason
                == aiplatform.protos.Prediction.FinishReason.SAFETY
            ):
                # This indicates the candidate itself was blocked.
                safety_ratings = []
                for rating in candidate.safety_ratings:
                    safety_ratings.append(
                        SafetyRating(
                            category=rating.category.name,
                            probability=rating.probability.name,
                        )
                    )
                return SafetyResult(blocked=True, safety_ratings=safety_ratings)
            else:
                safety_ratings = []
                for rating in candidate.safety_ratings:
                    safety_ratings.append(
                        SafetyRating(
                            category=rating.category.name,
                            probability=rating.probability.name,
                        )
                    )
                return SafetyResult(blocked=False, safety_ratings=safety_ratings)

        return SafetyResult(
            blocked=False, safety_ratings=[]
        )  # No content, no block, no explicit ratings

    except Exception as e:
        # Handle cases where the prompt itself might be blocked before generation
        return SafetyResult(blocked=True, safety_ratings=[], error=str(e))
