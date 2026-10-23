import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def log_text_safety(log_messages: List[str], project_id: str, location: str = "us-central1") -> Dict[str, Any]:
    aiplatform.init(project=project_id, location=location)

    # Using a generative model for safety checks. 
    # Ensure the Vertex AI API is enabled and proper permissions are set.
    safety_attributes = []

    # Using a multimodal model that supports safety attributes in responses
    try:
        model = aiplatform.get_model_registry().get_latest_model("gemini-pro")
    except Exception as e:
        print(f"Warning: Could not get gemini-pro from model registry. Trying with GenerativeModel. Error: {e}")
        model = aiplatform.GenerativeModel("gemini-pro")

    results = {}
    for i, message in enumerate(log_messages):
        response = model.generate_content(
            message,
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
            ]
        )
        # The safety ratings are part of the candidate attributes
        # Accessing them directly might vary based on SDK version and model response structure
        # This is an illustrative way; actual access might require inspecting response.candidates[0].safety_ratings
        safety_ratings = []
        if response.candidates and hasattr(response.candidates[0], 'safety_ratings'):
            for rating in response.candidates[0].safety_ratings:
                safety_ratings.append({"category": rating.category.name, "probability": rating.probability.name})
        
        results[f"log_{i}"] = {"message": message, "safety_ratings": safety_ratings}

    return results
