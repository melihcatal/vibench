import os
from google.cloud import aiplatform
from typing import Dict, Any

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
LOCATION = "us-central1"  # Vertex AI region


def moderate_text_safety(text: str) -> Dict[str, Any]:
    if not PROJECT_ID:
        raise ValueError("GCP_PROJECT_ID must be set as an environment variable.")

    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    # Using the TextGenerationModel for content moderation
    # The 'gemini-pro' model can provide safety attributes in its response.
    model = aiplatform.preview.language_models.GenerativeModel("gemini-pro")

    # For content moderation, we can simply ask the model to analyze the text
    # and expect safety attributes in the response if configured.
    # Direct safety attribute extraction is usually part of model response object.
    response = model.generate_content(
        text,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE",
            },
        ],
    )

    # The safety attributes are usually accessible via response.prompt_feedback.safety_attributes
    # or similar structure, depending on the SDK version and model.
    # For gemini-pro, safety ratings are directly on the candidate object.
    safety_ratings = []
    if response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, "safety_ratings"):
                for rating in candidate.safety_ratings:
                    safety_ratings.append(
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name,
                        }
                    )

    return {"text": text, "safety_ratings": safety_ratings}
