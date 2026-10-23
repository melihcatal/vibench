from google.cloud import speech_v1p1beta1 as speech
from google.protobuf import json_format

# Google Cloud Speech-to-Text models (provided in speech_models.py)
import speech_models  # noqa

# Helper to deserialize incremental results and extract partial transcript
# This file focuses on extracting interim and final results from the StreamingRecognizeResponse protobuf.

def process_partial_response(response_proto):
    """Given a StreamingRecognizeResponse protobuf, return a list of (is_partial, transcript) tuples."""
    results = []
    for result in response_proto.results:
        if result.alternatives:
            transcript = result.alternatives[0].transcript
            is_partial = result.is_final is False
            results.append((is_partial, transcript))
            # Optional: enrich with word timestamps, speaker tags, etc. using speech_models.WordInfoParser
    return results

# Example usage with a protobuf response (pseudo):
# response = client.streaming_recognize(...)  # yields StreamingRecognizeResponse
# for is_partial, txt in process_partial_response(response):
#     print('Partial' if is_partial else 'Final', txt)
