import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from openai import OpenAI


OPENAI_MODEL = "gpt-5.4-mini"


@dataclass
class SafetyCheckResult:
    unsafe: bool
    categories: List[str]
    rationale: str
    raw_response: Dict[str, Any]


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def check_platform_output(output_text: str) -> SafetyCheckResult:
    client = _client()
    prompt = (
        "Analyze the following platform model output for unsafe content. "
        "Return only valid JSON with keys unsafe (boolean), categories (array of strings), "
        "and rationale (string). Unsafe content includes but is not limited to violence, self-harm, "
        "sexual content involving minors, illegal wrongdoing, hate or harassment, malware, and "
        "privacy violations. Output:\n\n" + output_text
    )
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a safety classification assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    data = json.loads(content)
    return SafetyCheckResult(
        unsafe=bool(data.get("unsafe", False)),
        categories=list(data.get("categories", [])),
        rationale=str(data.get("rationale", "")),
        raw_response=data,
    )


def main() -> None:
    import sys

    text = sys.stdin.read()
    result = check_platform_output(text)
    print(json.dumps({"unsafe": result.unsafe, "categories": result.categories, "rationale": result.rationale}))


if __name__ == "__main__":
    main()
