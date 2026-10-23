from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel
import os

def moderate_text(text: str, project_id: str, location: str = "us-central1") -> dict:
    """Moderates transcript text using Vertex AI's text-bison model for safety attributes.

    Args:
        text: The text to be moderated.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the Vertex AI model is hosted.

    Returns:
        A dictionary containing safety attributes and their scores.
    """
    aiplatform.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison") # Model family identifier

    # Using a structured prompt to ask for safety attributes
    prompt = f"""Analyze the following text for safety attributes like toxicity, profanity, hate speech, and sexual content. Provide a score (e.g., HIGH, MEDIUM, LOW, VERY LOW, NEGLIGIBLE) for each attribute found. If an attribute is not present, indicate 'NOT APPLICABLE'.

Text: """{text}"""

Safety Analysis:"""

    response = model.predict(
        prompt,
        safety_settings=[
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": 1 # BLOCK_LOW_AND_ABOVE
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": 1 # BLOCK_LOW_AND_ABOVE
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": 1 # BLOCK_LOW_AND_ABOVE
            },
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": 1 # BLOCK_LOW_AND_ABOVE
            },
        ]
    )

    # Parse the response to extract safety attributes. This is an example parsing,
    # as the model's response format might vary based on the prompt.
    moderation_results = {"raw_model_output": response.text}
    # A more robust parsing logic would be needed here based on expected output format.
    # For demonstration, we just return the raw text.
    print(f"Moderation results: {moderation_results}")
    return moderation_results

if __name__ == '__main__':
    # Example usage
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    text_to_moderate = "That's a really stupid idea, you idiot! I hate that so much."
    
    if PROJECT_ID == "your-gcp-project-id":
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual project ID.")
    else:
        print(f"Moderating text: \"{text_to_moderate}\"...")
        results = moderate_text(text_to_moderate, PROJECT_ID)
        print("--- Detailed Moderation Results ---")
        for k, v in results.items():
            print(f"{k}: {v}")
