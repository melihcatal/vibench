from typing import Dict, Any


def build_stt_config(
    speaker_labels: bool = False,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
) -> Dict[str, Any]:
    config: Dict[str, Any] = {
        "punctuate": punctuate,
        "format_text": format_text,
        "language_code": language_code,
    }
    if speaker_labels:
        config["speaker_labels"] = True
    return config
