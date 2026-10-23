import os
from typing import Dict
from dotenv import load_dotenv
from tisane import Service, Language

load_dotenv()
TISANE_API_KEY = os.getenv('TISANE_API_KEY')

service = Service(TISANE_API_KEY)

def moderate_text(text: str, language: Language = Language.ENGLISH) -> Dict:
    """
    Moderate raw user-provided text for profanity, hate, sexually explicit content,
    and other policy violations using Tisane's moderation API.
    Returns a dictionary with the moderation verdict and details.
    """
    result = service.analyze(
        text=text,
        language=language,
        settings={'policy': 'strict', 'categories': ['profanity', 'hate', 'sexual']}
    )
    return result

# Example usage (illustrative only)
if __name__ == '__main__':
    sample = "You are a total idiot and should be banned."
    print('Moderation result:', moderate_text(sample))

# End of claims_moderation.py