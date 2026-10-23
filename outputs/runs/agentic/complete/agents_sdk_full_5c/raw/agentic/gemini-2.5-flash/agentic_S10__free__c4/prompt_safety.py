import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
from typing import Dict, Any

def check_safety_attributes(text: str) -> Dict[str, Any]:
    """Checks prompts and generated text for unsafe content using Vertex AI Gemini safety attributes."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")
    
    # We are using generate_content to get safety attributes even if we don't care about the response text.
    # The safety attributes are part of the response metadata.
    response = model.generate_content(
        [Part.from_text(text)],
        safety_settings={
            "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
        },
        # Setting a low temperature and max_output_tokens if we still want a response,
        # but the primary goal here is safety attributes.
        generation_config={"temperature": 0.1, "max_output_tokens": 1} 
    )
    
    # The safety ratings are typically in the 'prompt_feedback' or 'candidates[0].safety_ratings'
    # For a simple check, we can just return the entire response object or parse it.
    if response.prompt_feedback:
        return {"prompt_feedback": [s.to_dict() for s in response.prompt_feedback.safety_ratings]}
    elif response.candidates:
        if response.candidates[0].safety_ratings:
            return {"candidate_safety_ratings": [s.to_dict() for s in response.candidates[0].safety_ratings]}
    return {"message": "No safety feedback or ratings found."}
