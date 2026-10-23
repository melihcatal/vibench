import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
)


def check_safety_attributes(project_id: str, location: str, model_name: str, text: str):
    """Checks platform model output for unsafe content using Google Cloud Vertex AI safety features."""
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)
    # To check safety attributes, we would typically get them from a response after a generation.
    # Here, we simulate generating content and then extracting safety ratings from the *response*.
    # In a real scenario, 'text' would be the output from a previous model generation.
    # For demonstration, we'll just run a dummy generation and show how to access safety_ratings
    # from the candidate object of the response.
    # A more direct safety check on arbitrary text would typically use a dedicated safety API if available for raw text.
    # For Vertex AI generative models, safety is part of the generation response.

    # Simulating a response to get safety attributes
    # The actual safety check would be performed on the 'text' input,
    # but the API typically provides safety ratings with the generation.
    # For simplicity, we'll just show how to structure the call if 'text' was part of a generation.
    response = model.generate_content(
        [text],  # Treating the input 'text' as the content to be evaluated for safety
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        },
    )

    safety_feedback = []
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        safety_feedback.append(
            {
                "type": "prompt_feedback",
                "ratings": [
                    {"category": r.category.name, "probability": r.probability.name}
                    for r in response.prompt_feedback.safety_ratings
                ],
            }
        )

    for candidate in response.candidates:
        if candidate.safety_ratings:
            safety_feedback.append(
                {
                    "type": "candidate_output",
                    "content": candidate.text,
                    "ratings": [
                        {"category": r.category.name, "probability": r.probability.name}
                        for r in candidate.safety_ratings
                    ],
                }
            )

    return safety_feedback
