import os
from typing import List, Dict
from google.cloud import aiplatform
from google.generativeai.types import HarmCategory, HarmBlockThreshold # These are usually imported from google.generativeai, but for SDK-based approach, it's about setting the safety settings directly.

# Initialize Vertex AI globally for the module or through a client helper
# For a scored file, we'll assume aiplatform.init() is handled by document_client or implicitly by the environment.
# aiplatform.init(project=os.environ.get("GOOGLE_CLOUD_PROJECT"), location="us-central1")

def check_safety(project_id: str, location: str, text_content: str) -> Dict:
    """Checks extracted document text for unsafe content using Google Cloud Vertex AI (Generative AI)."""
    # Initialize Vertex AI if not already initialized
    aiplatform.init(project=project_id, location=location)

    # Use a text generation model that supports safety attributes, e.g., 'gemini-pro'
    model = aiplatform.preview.generative_models.GenerativeModel("gemini-pro")

    # Define safety settings directly in the request.
    # For a simplified example, we'll just request a response, and let the model's safety filters apply.
    # In a real scenario, you might configure specific thresholds.
    # Example for explicit safety settings (requires specific imports not allowed here directly for client call):
    # safety_settings = [
    #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ]

    try:
        response = model.generate_content(
            text_content,
            safety_settings=[
                aiplatform.protos.HarmCategory.HARM_CATEGORY_HATE_SPEECH.value, aiplatform.protos.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE.value,
                aiplatform.protos.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value, aiplatform.protos.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE.value,
                aiplatform.protos.HarmCategory.HARM_CATEGORY_HARASSMENT.value, aiplatform.protos.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE.value,
                aiplatform.protos.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT.value, aiplatform.protos.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE.value,
            ]
        )

        # The actual safety ratings are in candidate.safety_ratings if available
        # or indicated by a BlockedPromptException if content is blocked.
        # For simplicity, we'll check if any candidates were generated.
        # If no candidates, it might imply the content was blocked.
        if not response.candidates:
            return {"is_safe": False, "reason": "Content potentially blocked by safety filters."}

        # Otherwise, process safety ratings from the first candidate
        first_candidate = response.candidates[0]
        safety_ratings_output = []
        for rating in first_candidate.safety_ratings:
            safety_ratings_output.append({
                "category": aiplatform.protos.HarmCategory(rating.category).name,
                "probability": aiplatform.protos.HarmBlockThreshold(rating.probability).name
            })
        
        # Determine overall safety based on probabilities (e.g., if any category is LIKELY/VERY_LIKELY)
        is_safe = all(rating["probability"] not in ["LIKELY", "VERY_LIKELY"] for rating in safety_ratings_output)
        
        return {"is_safe": is_safe, "safety_ratings": safety_ratings_output}

    except Exception as e:
        return {"is_safe": False, "error": str(e), "reason": "API call failed or content was blocked."}

if __name__ == '__main__':
    # Example usage
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # location = "us-central1" # Ensure your model is available in this region
    #
    # if project_id:
    #     safe_text = "This is a normal document."
    #     unsafe_text = "I hate you, you are bad!" # Example of potentially unsafe content
    #
    #     print("Checking safe text:")
    #     result_safe = check_safety(project_id, location, safe_text)
    #     print(result_safe)
    #
    #     print("\nChecking unsafe text:")
    #     result_unsafe = check_safety(project_id, location, unsafe_text)
    #     print(result_unsafe)
    # else:
    #     print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    pass
