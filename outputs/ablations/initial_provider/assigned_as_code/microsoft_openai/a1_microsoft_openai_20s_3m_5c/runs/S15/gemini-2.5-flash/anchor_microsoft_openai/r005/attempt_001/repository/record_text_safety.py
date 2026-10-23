from google.cloud import aiplatform
import os

def check_text_safety(text_content, project_id=None, location=None):
    project_id = project_id or os.environ.get("GCP_PROJECT_ID")
    location = location or os.environ.get("GCP_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GCP_PROJECT_ID environment variable.")

    aiplatform.init(project=project_id, location=location)

    # For safety attributes, we can leverage the safety settings of generative models.
    # Using a generative model and accessing its safety attributes in the response.
    try:
        model = aiplatform.GenerativeModel("gemini-pro")
        response = model.generate_content(text_content, 
                                         safety_settings=[
                                             {
                                                 "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                                                 "threshold": "BLOCK_NONE"
                                             },
                                             {
                                                 "category": "HARM_CATEGORY_HARASSMENT",
                                                 "threshold": "BLOCK_NONE"
                                             },
                                             {
                                                 "category": "HARM_CATEGORY_HATE_SPEECH",
                                                 "threshold": "BLOCK_NONE"
                                             },
                                             {
                                                 "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                                                 "threshold": "BLOCK_NONE"
                                             },
                                         ])
        # The safety attributes are usually part of the response metadata.
        # This example assumes a structure where safety ratings are accessible.
        # Actual implementation might need to parse `response.prompt_feedback` or `response.candidates[0].safety_ratings`
        safety_ratings = []
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
            for rating in response.prompt_feedback.safety_ratings:
                safety_ratings.append({"category": rating.category.name, "probability": rating.probability.name})
        elif hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                if hasattr(candidate, 'safety_ratings') and candidate.safety_ratings:
                    for rating in candidate.safety_ratings:
                        safety_ratings.append({"category": rating.category.name, "probability": rating.probability.name})

        return {"status": "success", "safety_ratings": safety_ratings}
    except Exception as e:
        return {"status": "error", "message": str(e)}
