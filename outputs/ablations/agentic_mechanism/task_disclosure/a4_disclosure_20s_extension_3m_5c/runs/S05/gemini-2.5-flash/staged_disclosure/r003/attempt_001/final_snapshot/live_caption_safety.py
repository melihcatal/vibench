import vertexai
from vertexai.preview.generative_models import HarmCategory, HarmBlockThreshold, GenerativeModel

def check_safety(text: str) -> dict:
    """
    Checks live transcript text for unsafe content using Google Cloud Vertex AI's Generative AI Safety API.

    Args:
        text: The live transcript text to check.

    Returns:
        A dictionary containing safety attributes and scores.
    """
    # Initialize Vertex AI (replace with your project and location)
    vertexai.init(project="your-gcp-project-id", location="us-central1") 

    model = GenerativeModel("gemini-pro") # Using gemini-pro for content moderation

    # Configure safety settings to block harmful content
    safety_settings = {
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    response = model.generate_content(
        text,
        safety_settings=safety_settings
    )
    
    # You might want to parse response.prompt_feedback.safety_ratings
    # and response.candidates[0].safety_ratings for a detailed safety analysis.
    # For simplicity, this example returns a basic representation.
    
    safety_analysis = {
        "is_unsafe": False,
        "blocked_reason": None,
        "safety_ratings": []
    }

    if response.prompt_feedback.block_reason:
        safety_analysis["is_unsafe"] = True
        safety_analysis["blocked_reason"] = str(response.prompt_feedback.block_reason)
    
    if response.prompt_feedback.safety_ratings:
        safety_analysis["safety_ratings"] = [
            {"category": str(rating.category), "probability": str(rating.probability)}
            for rating in response.prompt_feedback.safety_ratings
        ]

    return safety_analysis

if __name__ == "__main__":
    # Example usage:
    transcript_text = "I hate you, you are so stupid!"
    safety_result = check_safety(transcript_text)
    print(f"Transcript: \"{transcript_text}\"")
    print(f"Safety Check Result: {safety_result}")

    transcript_text_safe = "Hello, how are you today?"
    safety_result_safe = check_safety(transcript_text_safe)
    print(f"Transcript: \"{transcript_text_safe}\"")
    print(f"Safety Check Result: {safety_result_safe}")
