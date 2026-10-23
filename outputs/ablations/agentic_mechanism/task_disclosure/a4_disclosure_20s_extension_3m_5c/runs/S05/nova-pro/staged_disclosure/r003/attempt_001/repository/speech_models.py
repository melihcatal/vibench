import os

from google.cloud import speech_v1p1beta1 as speech


def create_streaming_recognize_request(config, audio):
    return speech.StreamingRecognizeRequest(
        config=config,
        audio_content=audio
    )


def parse_streaming_recognize_response(response):
    results = []
    for result in response.results:
        alternatives = []
        for alternative in result.alternatives:
            alternatives.append({
                'transcript': alternative.transcript,
                'confidence': alternative.confidence
            })
        results.append({
            'is_final': result.is_final,
            'alternatives': alternatives
        })
    return results


def normalize_transcript(transcript):
    return transcript.lower().strip()