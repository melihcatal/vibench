from model_client import get_generative_model
from model_models import ModelRequest, ModelResponse
from vertexai.generative_models import (
    GenerationResponse,
    HarmCategory,
    HarmBlockThreshold,
)


def check_platform_output_safety(request: ModelRequest) -> ModelResponse:
    model = get_generative_model()
    # Configure safety settings for the request
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    response: GenerationResponse = model.generate_content(
        request.prompt, safety_settings=safety_settings, **request.kwargs
    )

    safety_attributes = []
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_attributes.append(
                {
                    "category": rating.category.name,
                    "probability": rating.probability.name,
                    "blocked": rating.blocked,
                }
            )

    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_attributes.append(
                        {
                            "category": rating.category.name,
                            "probability": rating.probability.name,
                            "blocked": rating.blocked,
                        }
                    )

    return ModelResponse(
        text=response.text,
        raw_response=response._raw_response,
        metadata={"safety_attributes": safety_attributes},
    )
