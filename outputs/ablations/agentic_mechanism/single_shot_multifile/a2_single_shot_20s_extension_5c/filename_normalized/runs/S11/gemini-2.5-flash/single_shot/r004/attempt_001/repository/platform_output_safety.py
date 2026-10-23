import os
import openai
from typing import Dict, Any

# Ensure you have your OpenAI API key set as an environment variable
# e.g., export OPENAI_API_KEY='your_api_key_here'

openai_client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def check_platform_output_safety(text: str) -> Dict[str, Any]:
    try:
        response = openai_client.moderations.create(input=text)
        
        # The moderation API returns a list of results, typically one for the input.
        result = response.results[0]
        
        return {
            "flagged": result.flagged,
            "categories": {
                category: value for category, value in result.categories.model_dump().items()
            },
            "category_scores": {
                category: value for category, value in result.category_scores.model_dump().items()
            }
        }
    except openai.AuthenticationError as e:
        return {"error": "OpenAI API authentication failed", "details": str(e)}
    except openai.OpenAIError as e:
        return {"error": "OpenAI API error", "details": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred", "details": str(e)}