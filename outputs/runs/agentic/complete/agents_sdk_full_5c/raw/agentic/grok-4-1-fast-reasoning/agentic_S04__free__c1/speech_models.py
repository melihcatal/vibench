from typing import Dict, Any

def stt_config(speaker_diarization: bool = False) -> Dict[str, Any]:
    config = {
        'punctuate': True,
        'format_text': True,
    }
    if speaker_diarization:
        config['speaker_labels'] = True
    return config