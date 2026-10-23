import google.generativeai as genai
import os

def check_corpus_safety(text: str) -> dict:
    # This function would ideally use a dedicated content moderation API.
    # For demonstration, we use Gemini's safety settings as a proxy.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    try:
        # Attempt to generate content to trigger safety checks
        response = model.generate_content(
            f"Analyze the safety of the following text: {text}",
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
        )
        # The actual safety ratings are in the `prompt_feedback`
        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            return {rating.category.name: rating.probability.name for rating in response.prompt_feedback.safety_ratings}
        else:
            return {"status": "No specific safety concerns detected by prompt_feedback"}
    except Exception as e:
        return {"status": "Error during safety check", "details": str(e)}
