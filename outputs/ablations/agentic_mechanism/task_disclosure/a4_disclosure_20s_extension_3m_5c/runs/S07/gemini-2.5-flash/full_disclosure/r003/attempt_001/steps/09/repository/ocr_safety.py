import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
from vertexai.generative_models import HarmCategory, HarmProbability


def check_for_unsafe_content(document_text: str) -> dict:
    vertexai.init(project="YOUR_PROJECT_ID", location="YOUR_REGION")

    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [Part.from_text(document_text)]
    )

    safety_feedback = []
    is_unsafe = False

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_feedback.append({
                "category": rating.category.name,
                "probability": rating.probability.name
            })
            if rating.probability > HarmProbability.HARM_PROBABILITY_NEGLIGIBLE:
                is_unsafe = True
    
    # If the model blocked the content entirely, candidates will be empty
    if not response.candidates:
        is_unsafe = True

    return {
        "is_unsafe": is_unsafe,
        "safety_ratings": safety_feedback
    }
