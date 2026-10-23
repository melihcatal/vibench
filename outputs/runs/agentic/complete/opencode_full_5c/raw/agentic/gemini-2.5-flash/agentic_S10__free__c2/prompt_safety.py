import os
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)
from model_models import SafetyCheckRequest, SafetyCheckResponse


class VertexAISafetyClient:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        location = os.getenv("GOOGLE_CLOUD_LOCATION")
        if not project_id or not location:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID and GOOGLE_CLOUD_LOCATION environment variables must be set."
            )
        vertexai.init(project=project_id, location=location)
        self.model = GenerativeModel("gemini-pro")  # Using gemini-pro for safety checks

    def check_safety(self, request: SafetyCheckRequest) -> SafetyCheckResponse:
        # Vertex AI GenerativeModel has built-in safety attributes in the response
        # We can simulate a check by trying to generate content and inspecting the prompt_feedback
        # For a more explicit safety check, one might use a dedicated safety model if available,
        # or rely on the content filtering during generation.

        # This is a simplified check. A real-world scenario might involve analyzing
        # response.prompt_feedback.safety_attributes if a generation was attempted.

        # For this example, we'll try to generate content with very strict safety settings
        # and infer safety based on whether it was blocked.

        # Set safety settings to block content at all harm categories at the lowest threshold
        safety_settings = {
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }

        try:
            # Try a very minimal generation to trigger safety checks
            responses = self.model.generate_content(
                request.text,
                safety_settings=safety_settings,
                generation_config={
                    "max_output_tokens": 1
                },  # Minimal output to just check input safety
            )
            # If no exception, it means the input was not blocked at the lowest threshold
            # This is a simplified interpretation.
            is_safe = True
            safety_attributes = {
                category.name: threshold.name
                for category, threshold in safety_settings.items()
            }  # Placeholder
            if responses.prompt_feedback and responses.prompt_feedback.block_reason:
                is_safe = False
                # More detailed safety_attributes could be extracted from prompt_feedback if available
                safety_attributes["block_reason"] = (
                    responses.prompt_feedback.block_reason.name
                )
                # If input was blocked, content will be empty. So, check feedback
                if responses.prompt_feedback.safety_ratings:
                    for rating in responses.prompt_feedback.safety_ratings:
                        safety_attributes[rating.category.name] = (
                            rating.probability.name
                        )

        except ResponseValidationError as e:
            # This exception might indicate blocking at the API level due to safety
            is_safe = False
            safety_attributes = {
                "error": str(e),
                "message": "Content generation was blocked due to safety concerns.",
            }

        return SafetyCheckResponse(is_safe=is_safe, safety_attributes=safety_attributes)


def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    client = VertexAISafetyClient()
    return client.check_safety(request)
