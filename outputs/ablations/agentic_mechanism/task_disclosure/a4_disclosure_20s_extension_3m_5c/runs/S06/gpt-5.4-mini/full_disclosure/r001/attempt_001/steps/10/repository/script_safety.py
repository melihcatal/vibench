import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-4.1-mini"


def check_script_safety(text: str, context: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    context_clause = f" Context: {context}." if context else ""
    prompt = (
        "Assess the following narration script for unsafe content, including hate, harassment, sexual content involving minors, "
        "self-harm encouragement, violence encouragement, illegal wrongdoing, privacy violations, or other disallowed content."
        f"{context_clause}"
        " Return a JSON object with keys: safe (boolean), categories (array of strings), rationale (string), and flagged_excerpt (string). "
        "Only analyze the script; do not rewrite it.\n\n"
        f"{text}"
    )
    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )
    return {"result": response.output_text.strip()}
