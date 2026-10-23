import re

def normalize_transcript(text):
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
    return text

def create_recognition_config(
    language_code="en-US",
    model="latest_long",
    enable_punctuation=True,
    encoding="LINEAR16",
    sample_rate_hertz=16000,
):
    return {
        "config": {
            "encoding": encoding,
            "sample_rate_hertz": sample_rate_hertz,
            "language_code": language_code,
            "model": model,
            "enable_automatic_punctuation": enable_punctuation,
        },
        "single_utterance": False,
    }