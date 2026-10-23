from typing import Dict, List
import google.generativeai as genai
import os


def record_text_safety(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Check user-generated document fields for unsafe content using Google's Generative AI."""
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    safety_results = []

    for doc in documents:
        text_fields = {k: v for k, v in doc["body"].items() if isinstance(v, str)}
        for field, text in text_fields.items():
            response = model.generate_content(
                f"Analyze the following text for unsafe content:\n\n{text}",
                safety_settings={
                    "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
                    "HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
                    "SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
                    "DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
                },
            )
            safety_results.append(
                {
                    "document_id": doc["id"],
                    "field": field,
                    "is_safe": not response.candidates[0].safety_ratings,
                    "safety_ratings": [
                        {"category": rating.category, "probability": rating.probability}
                        for rating in response.candidates[0].safety_ratings
                    ],
                }
            )

    return safety_results
