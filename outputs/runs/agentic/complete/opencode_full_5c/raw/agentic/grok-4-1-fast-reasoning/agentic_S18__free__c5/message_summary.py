import os
import sys
import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    if not input_data:
        print(json.dumps({"summary": "No input data"}))
        sys.exit(0)
    msg_data = json.loads(input_data)
    data_str = msg_data.get("data", "{}")
    try:
        payload = json.loads(data_str)
    except json.JSONDecodeError:
        payload = {}
    content = payload.get("content", "")
    if not content:
        output = msg_data.copy()
        output["summary"] = "No content to summarize"
        print(json.dumps(output))
        sys.exit(0)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this message concisely:\\n\\n{content[:4000]}",
            }
        ],
        max_tokens=100,
        temperature=0.5,
    )
    summary = response.choices[0].message.content.strip()
    output = msg_data.copy()
    output["summary"] = summary
    print(json.dumps(output))
