from google import genai

def check_platform_output_safety(payload, config):
    with genai.Client(vertexai=True, project=config["project_id"], location=config["location"]) as client:
        response = client.models.generate_content(model=config["model_id"], contents=payload["text"])
    
    safety_attributes = []
    if response.candidates:
        for candidate in response.candidates:
            if candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    safety_attributes.append(rating.to_dict())
    
    return {"text": response.text or "", "safety_attributes": safety_attributes}
