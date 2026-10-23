import os
import json
from openai import OpenAI
from typing import Dict, Any
import model_client
import model_models


def extract_json(text: str, instructions: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = model_client.get_default_model()
    system_prompt = "You are a JSON extractor. Always respond with valid JSON matching the instructions. No extra text."
    user_prompt = f"""Instructions: {instructions}

Text to extract from: {text}

Output ONLY valid JSON:"""
    messages = model_models.build_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=0.0, max_tokens=2000
    )
    content = response.choices[0].message.content.strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from LLM response: {e}")
