import os
import google.generativeai as genai


def check_script_safety(script_text: str) -> dict:
    """Checks narration scripts for unsafe content using Google Cloud Generative AI.\n\n    This function uses a generative model to attempt to identify unsafe content
    by checking the model's safety feedback on the provided script text.
    """
    # Ensure the GOOGLE_API_KEY environment variable is set.
    # In a real application, consider more secure ways to manage API keys.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        # If GOOGLE_API_KEY is not set, provide a dummy response or raise an error
        return {
            "flagged": True,
            "categories": ["ENVIRONMENT_ERROR"],
            "score": 1.0,
            "detail": "GOOGLE_API_KEY not set",
        }

    genai.configure(api_key=api_key)

    # Use a concrete model identifier for content analysis.
    # 'gemini-pro' is chosen as a general-purpose model.
    model = genai.GenerativeModel("gemini-pro")  # Concrete model identifier

    try:
        # Attempt to generate a response from the script, or just pass it through
        # and check the prompt_feedback for safety attributes.
        # This approach leverages the built-in safety filters of the generative model.
        response = model.generate_content(
            script_text,
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

        if response.prompt_feedback and response.prompt_feedback.safety_ratings:
            flagged = False
            categories = []
            scores = []
            for rating in response.prompt_feedback.safety_ratings:
                # If the probability is HIGH or MEDIUM, consider it flagged.
                if rating.probability in ["HIGH", "MEDIUM"]:
                    flagged = True
                    categories.append(rating.category.name)
                    scores.append(
                        1.0 if rating.probability == "HIGH" else 0.5
                    )  # Assign scores for demonstration

            if flagged:
                return {
                    "flagged": True,
                    "categories": categories,
                    "score": max(scores),
                    "detail": str(response.prompt_feedback),
                }
            else:
                return {
                    "flagged": False,
                    "categories": [],
                    "score": 0.0,
                    "detail": str(response.prompt_feedback),
                }
        else:
            # No safety feedback, assume safe or unable to assess directly.
            return {
                "flagged": False,
                "categories": [],
                "score": 0.0,
                "detail": "No specific safety feedback from model.",
            }

    except Exception as e:
        # Handle potential errors during content generation/safety check
        return {
            "flagged": True,
            "categories": ["PROCESSING_ERROR"],
            "score": 1.0,
            "detail": str(e),
        }
