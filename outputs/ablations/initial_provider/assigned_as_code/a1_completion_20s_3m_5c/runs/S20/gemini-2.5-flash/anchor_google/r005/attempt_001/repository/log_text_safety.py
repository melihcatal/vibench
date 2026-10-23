from google.cloud import aiplatform
import os

def check_log_text_safety(project_id: str, location: str, log_message: str) -> dict:
    # Initialize the AI Platform client
    aiplatform.init(project=project_id, location=location)

    # Use the Gemini Pro model for safety checking
    model_name = "gemini-pro"
    model = aiplatform.preview.generative_models.GenerativeModel(model_name)

    # The generate_content method automatically includes safety attributes in the response
    response = model.generate_content(log_message)

    safety_attributes = {"categories": [], "scores": []}
    if response._candidate_data and response._candidate_data[0].safety_ratings:
        for rating in response._candidate_data[0].safety_ratings:
            safety_attributes["categories"].append(rating.category.name)
            safety_attributes["scores"].append(rating.probability.name)

    # You can also check if the content was blocked
    blocked = response.prompt_feedback and response.prompt_feedback.block_reason is not None

    return {"log_message": log_message, "safety_attributes": safety_attributes, "blocked": blocked}
