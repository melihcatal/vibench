from google.cloud import aiplatform
from typing import List, Dict, Any

def moderate_batch_with_google(text_contents: List[str]) -> List[Dict[str, Any]]:
    aiplatform.init(project="YOUR_GOOGLE_CLOUD_PROJECT", location="us-central1")

    model_name = "gemini-pro"
    model = aiplatform.PreviewModel.from_pretrained(model_name)

    results = []
    for text_content in text_contents:
        try:
            response = model.predict(text_content)
            safety_attributes = {}
            if hasattr(response, 'safety_attributes'):
                safety_attributes = response.safety_attributes.to_dict()
            elif hasattr(response, 'candidates') and response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
                safety_ratings = [
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name,
                        "blocked": rating.blocked
                    }
                    for rating in response.candidates[0].safety_ratings
                ]
                safety_attributes["safety_ratings"] = safety_ratings
            else:
                safety_attributes["message"] = "No explicit safety attributes found in response, but text was processed."

            results.append({
                "text": text_content,
                "moderation_result": safety_attributes,
                "provider": "Google Vertex AI"
            })
        except Exception as e:
            results.append({
                "text": text_content,
                "error": str(e),
                "provider": "Google Vertex AI"
            })
    return results

