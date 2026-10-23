import os
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)
from typing import Dict, Any


class VendorTextSafety:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")

        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID environment variable not set for Vertex AI."
            )

        vertexai.init(project=project_id, location=location)
        # Using a generative model to evaluate text against safety attributes
        self.model = GenerativeModel("gemini-pro")

    def moderate_text(self, text_to_moderate: str) -> Dict[str, Any]:
        # The prompt itself is less important than the safety settings for moderation
        # We just need to pass the text through the model with safety settings applied
        try:
            response = self.model.generate_content(
                text_to_moderate,
                safety_settings={
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                },
            )
            # If the content is blocked, response.text might not exist
            # We check for prompt_feedback which contains safety_ratings
            safety_ratings = []
            if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                for rating in response.prompt_feedback.safety_ratings:
                    safety_ratings.append(
                        {
                            "category": str(rating.category).split(".")[
                                -1
                            ],  # Extract enum name
                            "probability": str(rating.probability).split(".")[
                                -1
                            ],  # Extract enum name
                            "blocked": rating.blocked,
                        }
                    )

            if response.text:
                return {
                    "moderated_text": response.text,
                    "safety_ratings": safety_ratings,
                    "blocked": False,
                }
            else:
                # If response.text is empty, it means it was blocked by safety settings
                return {
                    "moderated_text": "[Content Blocked]",
                    "safety_ratings": safety_ratings,
                    "blocked": True,
                }

        except Exception as e:
            return {
                "moderated_text": text_to_moderate,
                "safety_ratings": [],
                "blocked": False,
                "error": str(e),
            }
