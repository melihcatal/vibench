import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory as GenHarmCategory, HarmProbability as GenHarmProbability
from google.generativeai.generative_models import GenerativeModel

from safety_models import ModerationResult, ModerationScore, HarmCategory

def moderate_text(text: str) -> ModerationResult:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY must be set for Google Generative AI (PaLM/Gemini API).")
    
    genai.configure(api_key=api_key)
    
    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        text,
        safety_settings=[
            {"category": GenHarmCategory.HARM_CATEGORY_HARASSMENT, "threshold": GenHarmProbability.HARM_PROBABILITY_UNSPECIFIED},
            {"category": GenHarmCategory.HARM_CATEGORY_HATE_SPEECH, "threshold": GenHarmProbability.HARM_PROBABILITY_UNSPECIFIED},
            {"category": GenHarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, "threshold": GenHarmProbability.HARM_PROBABILITY_UNSPECIFIED},
            {"category": GenHarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, "threshold": GenHarmProbability.HARM_PROBABILITY_UNSPECIFIED},
        ]
    )

    safety_scores = []
    category_mapping = {
        GenHarmCategory.HARM_CATEGORY_HARASSMENT: HarmCategory.HARASSMENT,
        GenHarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmCategory.HATE_SPEECH,
        GenHarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmCategory.SEXUAL,
        GenHarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmCategory.DANGEROUS_CONTENT,
    }

    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        for rating in response.prompt_feedback.safety_ratings:
            mapped_category = category_mapping.get(rating.category)
            if mapped_category:
                safety_scores.append(ModerationScore(category=mapped_category, score=rating.probability_score))

    return ModerationResult(text=text, scores=safety_scores, decision="SCORED")