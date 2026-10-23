import os
from typing import Dict


def load_config() -> Dict[str, str]:
    return {
        "GOOGLE_PROJECT_ID": os.getenv("GOOGLE_PROJECT_ID"),
        "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "XAI_API_KEY": os.getenv("XAI_API_KEY"),
    }
