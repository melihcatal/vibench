import os
import sys
import json
from google.cloud import translate_v2 as translate

client = translate.Client()

TARGET_LANG = os.getenv("TARGET_LANG", "es")

if __name__ == "__main__":
    input_data = sys.stdin.read().strip()
    if not input_data:
        print(json.dumps({"translated": "No input data"}))
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
        output["translated"] = "No content"
        print(json.dumps(output))
        sys.exit(0)
    result = client.translate(content, target_language=TARGET_LANG)
    translated = result["translatedText"]
    output = msg_data.copy()
    output["translated"] = translated
    print(json.dumps(output))
