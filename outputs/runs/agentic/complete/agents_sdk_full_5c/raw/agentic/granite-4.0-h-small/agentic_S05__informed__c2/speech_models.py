# [HELPER]
# speech_models.py
# Local utilities for normalizing request payloads and parsing responses for Amazon Transcribe Streaming
# Provider: Amazon Transcribe Streaming (boto3 SDK)
import json
from typing import Dict, Any, List, Optional

class SpeechModels:
    """Helper class to map common concepts across the streaming API."""

    @staticmethod
    def build_start_request(language_code: str = 'en-US',
                            enable_punctuation: bool = False,
                            sample_rate: int = 16000,
                            encoding: str = 'pcm') -> Dict[str, Any]:
        """
        Construct the payload expected by start_stream_transcription.
        Returns a dict ready for boto3.
        """
        return {
            'LanguageCode': language_code,
            'EnablePunctuation': enable_punctuation,
            'MediaSampleRateHertz': sample_rate,
            'MediaEncoding': encoding,
        }

    @staticmethod
    def parse_transcription_result(result_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract interim and final transcriptions from the raw result payload.
        Transcribe returns a JSON payload that may contain 'InterimResults' and/or 'Results'.
        Returns a flat list of dicts with keys: transcript, is_final.
        """
        items = []
        if 'InterimResults' in result_payload:
            for interim in result_payload['InterimResults']:
                alt = interim.get('Alternatives', [{}])[0]
                items.append({'transcript': alt.get('Transcript', ''), 'is_final': False})
        if 'Results' in result_payload:
            for final in result_payload['Results']:
                alt = final.get('Alternatives', [{}])[0]
                items.append({'transcript': alt.get('Transcript', ''), 'is_final': True})
        return items

    @staticmethod
    def augment_with_confidence(result_items: List[Dict[str, Any]],
                                raw_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        If confidence scores are present, attach them to each transcript item.
        Transcribe may include a 'Confidence' field under Alternatives.
        """
        for i, item in enumerate(result_items):
            # Find matching alternative in raw result for confidence if available
            raw_alternatives = raw_result.get('Results', [])
            confidence = None
            for alt in raw_alternatives:
                trans = alt.get('Transcript', '')
                if trans == item['transcript']:
                    confidence = alt.get('Confidence')
                    break
            item['confidence'] = confidence
        return result_items

if __name__ == '__main__':
    # Simple demo
    data = SpeechModels.build_start_request(language_code='fr-FR', enable_punctuation=True)
    print('Start request:', json.dumps(data, indent=2))

    # Simulate a result payload
    sample = {
        'InterimResults': [
            {
                'Alternatives': [{
                    'Transcript': 'Bonjour le monde',
                    'Confidence': '0.92'
                }]
            }
        ],
        'Results': [
            {
                'Alternatives': [{
                    'Transcript': 'Au revoir',
                    'Confidence': '0.88'
                }]
            }
        ]
    }
    items = SpeechModels.parse_transcription_result(sample)
    print('Parsed items before confidence:', items)
    enriched = SpeechModels.augment_with_confidence(items, sample)
    print('Parsed items with confidence:', enriched)
