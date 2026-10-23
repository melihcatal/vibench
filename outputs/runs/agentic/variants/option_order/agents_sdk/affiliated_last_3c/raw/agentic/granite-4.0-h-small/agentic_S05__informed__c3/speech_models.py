# [HELPER] speech_models.py
import json
from typing import Any, Dict

# Conrete provider: Amazon Transcribe Streaming
# Provides normalization utilities for streaming responses and temporary model handling

# Supported model families for Amazon Transcribe Streaming
AVAILABLE_MODELS = {
    'general': 'Wideband',
    'medical': 'Medical',
    'audio': 'General',
}

def normalize_transcribe_event(event: dict) -> Dict[str, Any]:
    """Convert raw Transcribe streaming event to consistent dictionary."""
    result = {
        'type': event.get('Type', 'unknown'),
        'transcript': '',
        'is_partial': False,
    }
    # Transcribe events contain a Results list; we aggregate alternatives
    results = event.get('Results', [])
    if results:
        # Only the first alternative is used for simplicity
        alt = results[0].get('Alternatives', [{}])[0]
        result['transcript'] = alt.get('Transcript', '')
        # Transcribe marks partial results with specific event type
        result['is_partial'] = event.get('Type') == 'TranscriptionCompletePartial'
    return result


def apply_model_settings(config: dict, model: str) -> dict:
    """Inject Amazon Transcribe model setting into streaming config."""
    if model not in AVAILABLE_MODELS:
        raise ValueError(f'Model {model} not supported')
    config['Specialty'] = 'medical' if model == 'medical' else 'general'
    return config

if __name__ == '__main__':
    example_event = {
        'Type': 'TranscriptionCompletePartial',
        'TranscriptId': 'abc123',
        'Results': [{
            'Alternatives': [{
                'Transcript': 'This is a test sentence.'
            }]
        }]
    }
    norm = normalize_transcribe_event(example_event)
    print('Normalized event:', norm)
    cfg = apply_model_settings({'LanguageCode': 'en-US'}, 'medical')
    print('Config with medical model:', cfg)
