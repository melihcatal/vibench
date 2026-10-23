from google.cloud import aiplatform

def check_secret_label_safety(text: str, project_id: str, location: str) -> dict:
    aiplatform.init(project=project_id, location=location)
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")
    response = model.generate_content([f"Analyze the following text for safety concerns: {text}"])
    
    safety_attributes = {
        "harm_category": {
            category.name: category.probability.name
            for category in response.candidates[0].safety_ratings
        },
        "blocked": response.candidates[0].safety_ratings[0].blocked # If any harm category is BLOCK_LIKELY or higher
    }
    return safety_attributes
