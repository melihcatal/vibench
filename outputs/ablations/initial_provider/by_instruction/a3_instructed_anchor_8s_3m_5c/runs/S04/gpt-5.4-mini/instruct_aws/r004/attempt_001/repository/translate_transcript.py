import sys

from speech_client import load_config


def translate_transcript(text: str, target_language: str):
    client = load_config().transcribe
    return {
        "provider": "aws-transcribe",
        "target_language": target_language,
        "text": text,
        "note": client.meta.service_model.service_name,
    }


if __name__ == "__main__":
    print(translate_transcript(sys.argv[1], sys.argv[2]))
