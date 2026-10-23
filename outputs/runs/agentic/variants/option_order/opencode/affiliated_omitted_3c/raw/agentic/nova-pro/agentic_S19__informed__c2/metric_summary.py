import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

from anthropic import Anthropic

client = Anthropic(api_key=ANTHROPIC_API_KEY)
