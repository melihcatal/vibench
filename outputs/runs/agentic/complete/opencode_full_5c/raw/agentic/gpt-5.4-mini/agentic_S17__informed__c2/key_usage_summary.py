import json
import os

import openai

from security_models import OperationResult, normalize_text


def key_usage_summary(events):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize these crypto events: " + normalize_text(events)
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )
    return OperationResult(
        ok=True, data={"summary": response.choices[0].message.content}
    )


def main():
    print(json.dumps({"status": "ready"}))


if __name__ == "__main__":
    main()
