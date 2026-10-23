import os
import google.generativeai as genai

class ContentSafety:
    def __init__(self):
        # API key should be set as an environment variable
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

    def check_unsafe_content(self, text: str):
        """
        Checks the given text for unsafe content using Google's Generative AI.
        """
        try:
            response = self.model.generate_content(
                text,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                    },
                ],
            )
            # If the response has a prompt_feedback field and it indicates safety_ratings,
            # then content was blocked.
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.safety_ratings:
                blocked = False
                for rating in response.prompt_feedback.safety_ratings:
                    if rating.blocked:
                        blocked = True
                        break
                if blocked:
                    return {"unsafe": True, "details": [r.to_dict() for r in response.prompt_feedback.safety_ratings]}
            return {"unsafe": False, "details": []}
        except Exception as e:
            # Handle cases where content generation is blocked or other API errors
            return {"unsafe": True, "details": f"Content generation blocked or API error: {e}"}

