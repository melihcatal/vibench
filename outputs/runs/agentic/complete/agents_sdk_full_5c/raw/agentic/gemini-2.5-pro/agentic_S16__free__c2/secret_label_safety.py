import os
import cohere
from typing import List

def check_secret_label_safety(labels: List[str]) -> dict:
    """
    Uses Cohere to check if secret labels contain potentially unsafe text.
    
    Args:
        labels: A list of secret labels or notes to check.
        
    Returns:
        A dictionary with labels as keys and their safety classification.
    """
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    if not cohere_api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set.")
        
    co = cohere.Client(cohere_api_key)
    
    results = {}
    
    try:
        # Using the "classify" endpoint to check for custom classes.
        # Here we'll just use a generic model to check for something like toxicity
        # as a proxy for unsafe content. A real use case might use a fine-tuned model.
        response = co.classify(
            model='embed-english-v2.0', # Using a base model for classification
            inputs=labels,
            examples=[
                cohere.ClassifyExample(text="private key for prod", label="unsafe"),
                cohere.ClassifyExample(text="prod db password", label="unsafe"),
                cohere.ClassifyExample(text="ssh-key-value", label="unsafe"),
                cohere.ClassifyExample(text="api-token-for-billing", label="safe"),
                cohere.ClassifyExample(text="database connection string", label="safe"),
                cohere.ClassifyExample(text="service_api_key", label="safe"),
            ]
        )
        
        for classification in response.classifications:
            results[classification.input] = classification.prediction

    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        return {label: "error" for label in labels}

    return results
