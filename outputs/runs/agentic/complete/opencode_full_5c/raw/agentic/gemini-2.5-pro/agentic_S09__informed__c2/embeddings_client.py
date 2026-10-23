import os
import openai

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

client = openai.OpenAI(api_key=api_key)
