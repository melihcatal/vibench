from document_client import get_generative_model_client
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)


def moderate_vendor_notes(project_id: str, location: str, text: str) -> dict:
    model: GenerativeModel = get_generative_model_client(
        project_id, location, model_name="gemini-1.5-flash-001"
    )

    # Safety settings to block harmful content. These are example settings.
    # The actual behavior depends on the model and project configuration.
    safety_settings = [
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT,
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ]

    try:
        response = model.generate_content(
            text,
            safety_settings=safety_settings,
            generation_config={
                "temperature": 0.0,
                "max_output_tokens": 1,  # We only care about blocking, not content generation
            },
        )

        # If the response is blocked, access the prompt_feedback
        if (
            response._raw_response.prompt_feedback
            and response._raw_response.prompt_feedback.block_reason
        ):
            return {
                "is_safe": False,
                "block_reason": str(
                    response._raw_response.prompt_feedback.block_reason
                ),
                "safety_ratings": [
                    {
                        "category": str(sr.category),
                        "probability": str(sr.probability),
                        "blocked": sr.blocked,
                    }
                    for sr in response._raw_response.prompt_feedback.safety_ratings
                ],
            }
        else:
            # If no block reason, content is considered safe under the applied settings
            return {
                "is_safe": True,
                "block_reason": None,
                "safety_ratings": [
                    {
                        "category": str(sr.category),
                        "probability": str(sr.probability),
                        "blocked": sr.blocked,
                    }
                    for sr in response._raw_response.candidates[0].safety_ratings
                ]
                if response._raw_response.candidates
                else [],
            }
    except Exception as e:
        # Catch potential exceptions where content is blocked before a candidate is generated
        return {
            "is_safe": False,
            "block_reason": "Error during moderation or content blocked by safety filters prior to response generation.",
            "error": str(e),
        }
