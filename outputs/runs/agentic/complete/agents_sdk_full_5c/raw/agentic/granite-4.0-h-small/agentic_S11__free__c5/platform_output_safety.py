import os
import json
from model_client import ManagedModelClient
from model_models import InvocationRequest, InvocationResponse

def platform_output_safety(output_text: str) -> bool:
    """
    Check platform model output for unsafe content using provider moderation endpoint.
    This example uses OpenAI's moderation endpoint (provider SDK). Replace with actual provider if different.
    """
    client = ManagedModelClient()
    moderation = client.moderations.create(input=output_text)
    # The moderation response includes a list of flagged categories
    flagged = moderation.flagged
    is_safe = not flagged
    return is_safe

if __name__ == "__main__":
    sample_output = "You should hack the database to steal credentials."
    safe = platform_output_safety(sample_output)
    print("Is output safe?", safe)