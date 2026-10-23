import os
import cohere
from cohere.responses.classify import Example

from security_models import SafetyClassification

def check_secret_label_safety(text_to_check: str) -> SafetyClassification:
    """
    Uses the Cohere Classify endpoint to check if a secret label contains
    potentially unsafe or sensitive content.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    examples = [
        Example("prod-db-password", "safe"),
        Example("API key for Stripe", "safe"),
        Example("dev-cluster-admin", "safe"),
        Example("shared-staging-secret", "safe"),
        Example("Contact: jane.doe@example.com", "unsafe"),
        Example("SSN: 999-99-9999", "unsafe"),
        Example("Internal project codename 'BlueHarvest'", "unsafe"),
        Example("Emergency key held by Bob", "unsafe"),
    ]

    try:
        response = co.classify(
            model="embed-english-light-v2.0",
            inputs=[text_to_check],
            examples=examples,
        )
        
        classification = response.classifications[0]
        return SafetyClassification(
            input_text=classification.input,
            classification=classification.prediction,
            confidence=classification.confidence
        )
    except Exception as e:
        print(f"Error during Cohere classification: {e}")
        raise
