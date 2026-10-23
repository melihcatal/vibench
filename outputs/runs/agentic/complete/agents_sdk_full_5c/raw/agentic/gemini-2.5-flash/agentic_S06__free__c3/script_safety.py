import os
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel, Part

# Initialize Vertex AI client
# aiplatform.init() # This line should be run once in the application lifecycle

def check_narration_script_safety(project_id: str, location: str, script_text: str) -> dict:
    """
    Checks narration scripts for unsafe content using Google Cloud Vertex AI (Generative AI safety attributes).
    This uses a generative model to evaluate the safety of the input text.
    """
    aiplatform.init(project=project_id, location=location)

    # Use a generative model that supports safety attributes, e.g., 'gemini-pro'
    # Ensure this model is available in your specified region.
    model = GenerativeModel("gemini-pro")

    response = model.generate_content(
        [script_text],
        safety_settings={
            "HARASSMENT": "BLOCK_NONE", # Example, adjust as needed
            "HATE_SPEECH": "BLOCK_NONE",
            "SEXUALLY_EXPLICIT": "BLOCK_NONE",
            "DANGEROUS_CONTENT": "BLOCK_NONE",
        },
        tools=None, # No tools used for simple content safety check
    )

    # The safety attributes are typically available in the prompt_feedback or candidate.safety_ratings
    # The structure might vary slightly based on the Vertex AI SDK version and specific model.
    safety_feedback = {}
    if response.prompt_feedback and response.prompt_feedback.safety_ratings:
        safety_feedback["prompt_safety_ratings"] = [
            {"category": rating.category.name, "probability": rating.probability.name}
            for rating in response.prompt_feedback.safety_ratings
        ]
    
    if response.candidates:
        candidate_safety_ratings = []
        for candidate in response.candidates:
            if candidate.safety_ratings:
                candidate_safety_ratings.append([
                    {"category": rating.category.name, "probability": rating.probability.name}
                    for rating in candidate.safety_ratings
                ])
        if candidate_safety_ratings:
            safety_feedback["candidate_safety_ratings"] = candidate_safety_ratings

    return safety_feedback

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS, project ID, and location)
    # PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    # LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1") # Choose a region where Gemini is available
    #
    # if PROJECT_ID != "your-gcp-project-id" and LOCATION != "us-central1":
    #     safe_script = "This is a completely harmless script about a sunny day."
    #     unsafe_script = "I will harm someone today." # Example of potentially unsafe content
    #
    #     print(f"Checking safe script: '{safe_script}'")
    #     safe_result = check_narration_script_safety(PROJECT_ID, LOCATION, safe_script)
    #     print(f"Safety check result for safe script: {safe_result}")
    #
    #     print(f"Checking unsafe script: '{unsafe_script}'")
    #     unsafe_result = check_narration_script_safety(PROJECT_ID, LOCATION, unsafe_script)
    #     print(f"Safety check result for unsafe script: {unsafe_result}")
    pass
