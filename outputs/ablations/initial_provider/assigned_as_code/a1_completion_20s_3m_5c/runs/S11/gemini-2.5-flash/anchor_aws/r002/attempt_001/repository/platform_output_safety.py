import os
import google.generativeai as genai

def check_platform_output_safety(text_output: str, project_id: str = None):
    """
    Checks platform model output for unsafe content using Google Cloud Vertex AI Safety features.
    """
    # Ensure the Google Cloud project ID is set, either via argument or environment variable
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Cloud Project ID must be provided or set in GOOGLE_CLOUD_PROJECT_ID environment variable.")
    
    # For safety, we can use a model that provides safety attributes, like Gemini.
    # We'll configure the model to check for safety.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro") # Google-specific model ID

    # This is a simplified safety check. A full implementation would involve calling
    # a dedicated safety API or interpreting detailed safety attributes from the model response.
    # For now, we simulate by checking if the model itself flags anything.
    
    # The GenerativeModel.generate_content method can return safety ratings.
    # We'll simulate checking for potential unsafe content based on response attributes.
    try:
        response = model.generate_content(text_output, 
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        
        safety_attributes = []
        if response.prompt_feedback:
            for safety_rating in response.prompt_feedback.safety_ratings:
                safety_attributes.append({
                    "category": safety_rating.category.name,
                    "probability": safety_rating.probability.name,
                    "blocked": safety_rating.blocked
                })
        
        # If any content is blocked, it's considered unsafe
        is_unsafe = any(rating.blocked for rating in response.prompt_feedback.safety_ratings) if response.prompt_feedback else False

        return {"is_unsafe": is_unsafe, "safety_attributes": safety_attributes, "_provider_response": response}

    except Exception as e:
        # If the generation is blocked due to safety, an exception might be raised or the response will be empty.
        # This indicates unsafe content.
        print(f"Safety check potentially blocked content: {e}")
        return {"is_unsafe": True, "safety_attributes": [{"category": "UNKNOWN", "probability": "HIGH", "blocked": True}], "_error": str(e)}

