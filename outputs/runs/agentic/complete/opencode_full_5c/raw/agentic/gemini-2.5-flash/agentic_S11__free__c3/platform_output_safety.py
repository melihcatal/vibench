import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, GenerationConfig
from model_client import get_vertex_ai_project_location
from model_models import PlatformSafetyCheckRequest, PlatformSafetyCheckResponse


def check_platform_output_safety(
    request: PlatformSafetyCheckRequest,
) -> PlatformSafetyCheckResponse:
    project, location = get_vertex_ai_project_location()
    vertexai.init(project=project, location=location)

    # Using the same model for safety checking for simplicity,
    # as Vertex AI's GenerativeModel responses include safety attributes.
    model = GenerativeModel(request.model_id)

    # We send the text to the model to get a response which includes safety attributes.
    # The actual generation part is not what we're interested in, but the safety_attributes.
    # A dummy generation config is used to ensure a response.
    dummy_generation_config = GenerationConfig(max_output_tokens=1)
    prompt_parts = [Part.from_text(request.text)]
    response = model.generate_content(
        prompt_parts, generation_config=dummy_generation_config
    )

    safety_attributes = {}
    is_safe = True

    if response.candidates:
        # Access safety ratings from the first candidate
        for rating in response.candidates[0].safety_ratings:
            safety_attributes[rating.category.name] = rating.probability.name
            if (
                rating.probability.value >= 4
            ):  # Assuming probability value 4 or higher means unsafe (HIGH or VERY_HIGH)
                is_safe = False

    return PlatformSafetyCheckResponse(
        text=request.text,
        is_safe=is_safe,
        safety_attributes=safety_attributes,
        provider="Google Cloud Vertex AI",
    )
