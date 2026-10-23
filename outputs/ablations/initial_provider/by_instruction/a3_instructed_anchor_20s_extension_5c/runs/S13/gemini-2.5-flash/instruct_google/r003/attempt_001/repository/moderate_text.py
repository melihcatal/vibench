import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, HarmCategory, HarmBlockThreshold

def moderate_text(text: str) -> dict:
    """
    Scores user text for unsafe or policy-violating content using Google Vertex AI.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = "gemini-pro"

    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    response = model.generate_content(
        [text],
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
        stream=False,
    )

    # Extract safety attributes from the response
    safety_ratings = []
    if hasattr(response, 'candidates') and response.candidates:
        for candidate in response.candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    safety_ratings.append({
                        "category": rating.category.name,
                        "probability": rating.probability.name,
                        "blocked": rating.blocked
                    })

    return {"safety_ratings": safety_ratings}
