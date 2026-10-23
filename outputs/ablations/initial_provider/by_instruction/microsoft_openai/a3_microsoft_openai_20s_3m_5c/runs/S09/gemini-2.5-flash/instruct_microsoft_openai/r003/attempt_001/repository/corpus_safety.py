import os
from google.cloud import aiplatform
from typing import List, Dict, Any

def check_corpus_safety(texts: List[str], project_id: str, location: str) -> Dict[str, Any]:
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel(model_name="gemini-pro")
    
    safety_results = {}
    for i, text in enumerate(texts):
        response = model.generate_content(text, safety_settings={'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE'})
        safety_attributes = {
            category.category.name: category.probability.name
            for category in response.candidates[0].safety_ratings
        }
        safety_results[f"text_{i}"] = {
            "text": text,
            "safety_ratings": safety_attributes
        }
    return safety_results