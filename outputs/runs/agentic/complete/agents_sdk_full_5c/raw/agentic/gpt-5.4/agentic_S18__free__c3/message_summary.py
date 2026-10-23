from __future__ import annotations

from typing import Any, Dict, List
import os

from openai import OpenAI

from messaging_models import ProcessingResult, summarize_results


OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")



def summarize_message_processing(results: List[ProcessingResult]) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    aggregate = summarize_results(results)
    prompt = {
        "summary_request": "Summarize message processing results for operators.",
        "aggregate": aggregate,
        "details": [result.__dict__ for result in results],
    }
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "user",
                "content": [{"type": "input_text", "text": str(prompt)}],
            }
        ],
    )
    text = getattr(response, "output_text", "")
    return {"aggregate": aggregate, "summary": text}
