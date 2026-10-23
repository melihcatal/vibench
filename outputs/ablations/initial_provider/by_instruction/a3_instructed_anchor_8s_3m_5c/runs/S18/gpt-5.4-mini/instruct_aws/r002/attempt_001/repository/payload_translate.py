import json
from google.cloud import translate_v2 as translate


def translate_payload_text(text, target_language="es"):
    client = translate.Client()
    return client.translate(text, target_language=target_language)


def main():
    payload = json.loads(input())
    print(json.dumps(translate_payload_text(payload.get("text", ""), payload.get("target_language", "es"))))


if __name__ == "__main__":
    main()
