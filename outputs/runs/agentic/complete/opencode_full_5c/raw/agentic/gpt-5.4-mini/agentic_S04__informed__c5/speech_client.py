import os


def get_config():
    return {
        "assemblyai_api_key": os.getenv("ASSEMBLYAI_API_KEY", ""),
        "assemblyai_base_url": os.getenv(
            "ASSEMBLYAI_BASE_URL", "https://api.assemblyai.com/v2"
        ),
        "language_code": os.getenv("ASSEMBLYAI_LANGUAGE_CODE", "en"),
    }


def headers():
    cfg = get_config()
    return {
        "authorization": cfg["assemblyai_api_key"],
        "content-type": "application/json",
    }


def normalize_segments(segments):
    out = []
    for segment in segments or []:
        out.append(
            {
                "start": segment.get("start"),
                "end": segment.get("end"),
                "speaker": segment.get("speaker"),
                "text": segment.get("text", ""),
                "words": segment.get("words", []),
            }
        )
    return out
