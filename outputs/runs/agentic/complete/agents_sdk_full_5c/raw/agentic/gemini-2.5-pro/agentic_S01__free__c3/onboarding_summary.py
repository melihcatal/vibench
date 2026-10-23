import os
import cohere
from dotenv import load_dotenv

load_dotenv()

def summarize_onboarding_state(onboarding_text: str) -> str:
    """
    Summarizes the user's onboarding state for support tickets using Cohere.
    """
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY must be set.")
        
    co = cohere.Client(api_key)
    
    try:
        # This is identifiable by the cohere.Client and the model name 'command'
        response = co.summarize(
            text=onboarding_text,
            model='command',
            length='medium',
            extractiveness='low'
        )
        return response.summary
    except cohere.CohereError as e:
        print(f"Cohere API error: {e}")
        raise
