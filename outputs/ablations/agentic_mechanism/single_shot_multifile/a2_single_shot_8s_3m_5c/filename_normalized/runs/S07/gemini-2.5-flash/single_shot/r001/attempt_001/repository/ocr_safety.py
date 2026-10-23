from google.cloud.aiplatform import HarmCategory, HarmBlockThreshold
from document_client import get_text_generation_model
from document_models import SafetyCheckResult, SafetyAttribute

def check_text_safety(text: str) -> SafetyCheckResult:
    model = get_text_generation_model(model_name="gemini-pro")
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
    }
    response = model.predict(
        f"Analyze the following text for safety and summarize it briefly: {text}",
        safety_settings=safety_settings
    )
    safety_attributes: list[SafetyAttribute] = []
    is_safe = True
    safety_attributes_response = response.safety_attributes
    if safety_attributes_response:
        for i, category_name in enumerate(safety_attributes_response.categories):
            score = safety_attributes_response.scores[i]
            probability_str = "NEGLIGIBLE"
            if score > 0.8: probability_str = "VERY_LIKELY"
            elif score > 0.6: probability_str = "LIKELY"
            elif score > 0.4: probability_str = "MODERATELY_LIKELY"
            elif score > 0.2: probability_str = "UNLIKELY"
            safety_attributes.append(SafetyAttribute(category=category_name, probability=probability_str, severity=None))
        is_safe = not safety_attributes_response.blocked
    else:
        is_safe = True
    return SafetyCheckResult(
        safety_attributes=safety_attributes,
        is_safe=is_safe,
        raw_response=response._prediction_response.to_dict() if hasattr(response, '_prediction_response') else {}
    )