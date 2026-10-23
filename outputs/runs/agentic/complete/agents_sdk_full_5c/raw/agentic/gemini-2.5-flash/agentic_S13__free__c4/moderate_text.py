import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def moderate_text_content(project_id: str, location: str, text_content: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    response = model.generate_content(
        text_content,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
    
    # Accessing safety ratings from the candidate
    safety_ratings = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            safety_ratings[rating.category.name] = {
                "score": rating.score,
                "severity": rating.severity,
                "blocked": rating.blocked
            }
    return safety_ratings
