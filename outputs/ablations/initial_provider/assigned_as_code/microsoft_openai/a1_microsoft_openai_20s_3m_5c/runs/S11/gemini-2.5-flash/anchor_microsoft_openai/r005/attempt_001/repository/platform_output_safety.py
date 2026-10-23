from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold
import vertexai

def check_platform_output_safety(project_id: str, location: str, model_name: str, text_output: str):
    """
    Checks platform model output for unsafe content using Google Cloud Vertex AI's safety features.
    For demonstration, we re-run a generation with safety settings and check the response.
    In a real scenario, you might have a dedicated safety API.
    """
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel(model_name)

    # We can't directly "check" an existing output for safety with the generative_models SDK
    # in a standalone way. The safety settings are applied during generation.
    # To demonstrate safety features, we'll try to generate content with strict safety settings
    # and see if it's blocked. A more realistic "check output" would involve
    # sending the output to a dedicated content moderation API if available.

    # Here, we simulate by attempting a generation with the given text as a prompt
    # and observe if it gets blocked by safety filters.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    response = model.generate_content(
        text_output, # Use the output as a "prompt" to check its safety if it were generated
        safety_settings=safety_settings,
        stream=False
    )
    
    is_safe = True
    safety_ratings = []
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        is_safe = False
        # If the prompt itself (which is our output for checking) was blocked
        safety_ratings.append({
            "category": "PROMPT_BLOCKED",
            "threshold": str(response.prompt_feedback.block_reason),
            "severity": "HIGH" # Placeholder
        })
    elif response.candidates:
        for candidate in response.candidates:
            if candidate.finish_reason and candidate.finish_reason == 1: # FINISH_REASON_SAFETY
                is_safe = False
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_ratings.append({
                        "category": str(rating.category).split('.')[-1],
                        "threshold": str(rating.threshold).split('.')[-1],
                        "severity": str(rating.severity).split('.')[-1]
                    })
    
    return {"is_safe": is_safe, "safety_ratings": safety_ratings}
