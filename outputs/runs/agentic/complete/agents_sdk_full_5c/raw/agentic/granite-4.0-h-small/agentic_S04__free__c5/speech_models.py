from typing import Any, Dict

class TranscriptionJobRequest:
    """Helper to build a provider‑specific batch request object.
    
    Provider example: Google Cloud Speech batch model expects fields like
    'config' (recognitionConfig), 'audio' (inputAudio) and optional flags.
    """
    def __init__(self,
                 audio_uri: str,
                 model: str = None,
                 enable_diarization: bool = False,
                 enable_timestamps: bool = False,
                 **kwargs):
        # Build a dict that maps to the provider's REST/Proto schema
        self.config = {
            'model': model,
            'diarization_config': {
                'enable_speaker_diarization': enable_diarization,
            },
            'speech_contexts': kwargs.get('speech_contexts', []),
            'enable_word_time_offsets': enable_timestamps,
        }
        self.audio = {'uri': audio_uri}
        self.request = {
            'config': self.config,
            'audio': self.audio
        }

    @staticmethod
    def normalize(result: Any) -> str:
        """Convert provider response protobuf/dict into a plain string transcript.
        This function abstracts away differences across providers.
        """
        # Mock implementation for illustration
        if isinstance(result, dict) and 'results' in result:
            segments = [alt['transcript'] for res in result['results'] for alt in res['alternatives']]
            return ' '.join(segments)
        # If provider returns a protobuf, we would do: return result.transcript_text
        return result
