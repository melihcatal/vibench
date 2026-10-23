import os
from typing import List, Dict, Any
from google.cloud import aiplatform

def check_log_message_safety(project_id: str, location: str, log_messages: List[str]) -> List[Dict[str, Any]]:
    aiplatform.init(project=project_id, location=location)

    model = aiplatform.preview.language_models.TextGenerationModel.from_pretrained("gemini-pro")

    safety_results = []
    for message_text in log_messages:
        response = model.predict(
            message_text,
            max_output_tokens=1,
            temperature=0.0, # Not generating text, just getting safety attributes
        )
        
        # The safety_attributes are part of the response metadata for Gemini models
        # Note: The exact structure might vary slightly with SDK updates
        safety_attributes = {
            "categories": [],
            "scores": [],
            "blocked": False
        }

        # For Gemini models, safety attributes are usually in a structured format within the response
        if response.safety_attributes:
            sa = response.safety_attributes
            safety_attributes["categories"] = [attr.category.name for attr in sa.categories]
            safety_attributes["scores"] = [attr.score for attr in sa.categories]
            safety_attributes["blocked"] = sa.blocked
            
        safety_results.append({"message": message_text, "safety_attributes": safety_attributes})

    return safety_results

if __name__ == '__main__':
    PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT')  # e.g., your-gcp-project-id
    LOCATION = os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1') # e.g., us-central1

    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        example_log_messages = [
            "User 'evil_hacker' attempted unauthorized access from 1.2.3.4.",
            "System health check passed successfully.",
            "Potential SQL injection detected in query: SELECT * FROM users WHERE id='1 OR 1=1' -- ",
            "Comment from user: This is a perfectly safe message.",
            "System error: \'NoneType\' object has no attribute \'decode\'.",
        ]

        print("Checking log messages for unsafe content...")
        results = check_log_message_safety(PROJECT_ID, LOCATION, example_log_messages)

        for res in results:
            print(f"\nMessage: {res['message']}")
            print(f"Safety Attributes: {res['safety_attributes']}")
