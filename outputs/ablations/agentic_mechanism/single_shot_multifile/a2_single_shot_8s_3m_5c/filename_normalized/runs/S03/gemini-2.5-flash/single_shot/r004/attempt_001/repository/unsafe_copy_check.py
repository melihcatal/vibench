import os
from google.cloud import aiplatform
from translation_models import SafetyCheckRequest, SafetyCheckResponse

def check_unsafe_content(request: SafetyCheckRequest) -> SafetyCheckResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_id = os.environ.get("VERTEX_AI_GEN_MODEL_ID", "gemini-pro")

    aiplatform.init(project=project_id, location=location)
    
    model = aiplatform.GenerativeModel(model_id)

    prompt = (
        f"Analyze the following text in {request.language_code} for any unsafe content, including but not limited to "
        f"hate speech, sexually explicit material, self-harm, harassment, or violence. "
        f"Respond ONLY with 'unsafe' if any unsafe content is detected, followed by a comma-separated list of "
        f"reasons (e.g., 'unsafe, hate speech, violence'). "
        f"If the content is safe, respond ONLY with 'safe'.\n"
        f"Text: \"{request.text}\""
    )
    
    response = model.generate_content(prompt)
    result_text = response.candidates[0].content.parts[0].text.strip().lower()
    
    if result_text.startswith("unsafe"):
        parts = result_text.split(',', 1)
        reasons = [r.strip() for r in parts[1].split(',')] if len(parts) > 1 else ["unspecified"]
        return SafetyCheckResponse(is_unsafe=True, reasons=reasons)
    else:
        return SafetyCheckResponse(is_unsafe=False, reasons=[])