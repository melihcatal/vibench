import os
import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold

def moderate_text_with_vertex_ai(text_content: str) -> dict:
    """
    Moderates the given text content using Google Cloud Vertex AI's GenerativeModel.

    Args:
        text_content: The text string to be moderated.

    Returns:
        A dictionary containing the moderation response, including safety ratings.
    """
    # Initialize Vertex AI
    # Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION environment variables are set
    # or pass project and location explicitly to vertexai.init()
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1") # Default to us-central1
        if not project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
        vertexai.init(project=project_id, location=location)
    except Exception as e:
        return {"error": f"Vertex AI initialization failed: {e}. Please ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION are set."}

    model = GenerativeModel("gemini-pro")

    try:
        response = model.generate_content(
            [text_content],
            safety_settings={
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False,
        )

        # Extracting safety ratings from the response
        safety_ratings = []
        if response.candidates:
            for candidate in response.candidates:
                if candidate.safety_ratings:
                    for rating in candidate.safety_ratings:
                        safety_ratings.append({
                            "category": str(rating.category).split('.')[-1],
                            "threshold": str(rating.threshold).split('.')[-1],
                            "blocked": rating.blocked
                        })
        
        return {
            "moderation_status": "completed",
            "safety_ratings": safety_ratings,
            "full_response_text": response.text if response.candidates and response.candidates[0].content else ""
        }
    except Exception as e:
        return {"error": f"Text moderation failed: {e}"}

if __name__ == "__main__":
    # Example usage for moderating vendor notes
    vendor_note = "This is a test note. It contains some potentially harmful content like hate speech."
    
    # You need to set GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_REGION environment variables
    # e.g., export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    #       export GOOGLE_CLOUD_REGION="us-central1"
    
    moderation_result = moderate_text_with_vertex_ai(vendor_note)
    print("Moderation Result:")
    print(moderation_result)

    vendor_note_safe = "This is a perfectly safe vendor note about delivery details."
    moderation_result_safe = moderate_text_with_vertex_ai(vendor_note_safe)
    print("\nSafe Moderation Result:")
    print(moderation_result_safe)
