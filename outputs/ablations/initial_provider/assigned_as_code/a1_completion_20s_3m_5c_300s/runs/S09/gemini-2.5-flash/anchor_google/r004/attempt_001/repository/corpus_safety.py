import os
from typing import List, Dict
import google.generativeai as genai
from embeddings_models import GENAI_GENERATION_MODEL

def corpus_safety(payload: Dict, config: Dict = None) -> Dict:
    config = config or {}
    api_key = config.get("api_key") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found. Please set the environment variable or pass it to the client.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(GENAI_GENERATION_MODEL)

    texts_to_check = payload.get("texts", [])
    if not isinstance(texts_to_check, list) or not all(isinstance(t, str) for t in texts_to_check):
        raise ValueError("Payload must contain a 'texts' key with a list of strings.")

    safety_results = []
    for text in texts_to_check:
        try:
            # Generate content to implicitly trigger safety checks. The actual generated content is less important
            # than the safety feedback received in the response.
            response = model.generate_content(
                text,
                safety_settings=[
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                ]
            )
            # The prompt is sent, and the safety attributes are available in the response
            # if any blocking occurred or if specific attributes are present.
            # For this task, we want to report the safety feedback directly.
            safety_feedback = []
            if response._error:
                safety_feedback.append({"status": "ERROR", "message": str(response._error)})
            elif response.prompt_feedback and response.prompt_feedback.safety_ratings:
                for rating in response.prompt_feedback.safety_ratings:
                    safety_feedback.append({
                        "category": rating.category.name,
                        "probability": rating.probability.name,
                        "blocked": rating.blocked,
                    })
            else:
                safety_feedback.append({"status": "CLEAN", "message": "No explicit safety violations detected."})

            safety_results.append({"text": text, "safety_feedback": safety_feedback})

        except Exception as e:
            safety_results.append({"text": text, "safety_feedback": [{"status": "ERROR", "message": str(e)}]})

    return {"safety_checks": safety_results}
