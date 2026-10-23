import os
from ibm_watsonx_ai.services.emergency_uplift import HazardAssessment
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Configure guardrails client
guardrails = HazardAssessment(
    api_key=API_KEY,
    project_id=PROJECT_ID,
    url="https://api.us-south.watsonx.ai"
)

def corpus_safety(text: str) -> bool:
    """Check if corpus text is safe for embedding using Watsonx Guardrails."""
    assessment = guardrails.assess(text=text, category="TOXICITY")
    # Assuming the API returns a dict with a boolean 'pass' field
    return assessment.get('pass', False)
