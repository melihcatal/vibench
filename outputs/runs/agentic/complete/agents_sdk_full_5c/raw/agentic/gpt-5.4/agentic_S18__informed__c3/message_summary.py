from __future__ import annotations

from typing import Any, Dict, Iterable, List
import json
import os

from openai import OpenAI

from messaging_models import ProcessingSummary


MODEL_NAME = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")



def summarize_processing_results(results: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    result_list: List[Dict[str, Any]] = list(results)
    summary = ProcessingSummary(
        total=len(result_list),
        succeeded=sum(1 for item in result_list if item.get("status") == "succeeded"),
        failed=sum(1 for item in result_list if item.get("status") != "succeeded"),
        details=[f"{item.get('message_id', 'unknown')}: {item.get('status', 'unknown')}" for item in result_list],
    )

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0.2,
        messages=[
            {"role": "system", "content": "Summarize message processing outcomes for operators in 2-3 concise sentences."},
            {"role": "user", "content": json.dumps(summary.to_dict())},
        ],
    )
    return {
        "provider": "OpenAI",
        "model": MODEL_NAME,
        "summary": response.choices[0].message.content,
        "stats": summary.to_dict(),
    }
