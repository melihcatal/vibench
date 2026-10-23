import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def ocr_safety(text: str, project_id: str, location: str):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro") # Using gemini-pro for content moderation
    
    response = model.generate_content([text, "Check if this content is safe and does not contain harmful content."],
                                      safety_settings={})
    
    # The safety attributes are usually part of the response if any violations are detected.
    # For a more robust solution, one would parse response.candidates[0].safety_ratings
    # and provide a structured output.
    
    # For this example, we'll return a simplified response indicating if safety attributes are present
    # and the full response for detailed analysis.
    
    safety_attributes_present = False
    if response.candidates and response.candidates[0].safety_ratings:
        safety_attributes_present = True
        
    return {"is_safe": not safety_attributes_present, "safety_response": str(response)}
