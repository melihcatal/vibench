import json
import sys

from speech_client import load_config
from speech_models import segments_from_transcript, transcript_from_json


def timestamped_transcript(transcript_uri: str):
    import urllib.request

    with urllib.request.urlopen(transcript_uri) as response:
        data = response.read().decode("utf-8")
    results = transcript_from_json(data)
    return [segment.__dict__ for segment in segments_from_transcript(results)]


if __name__ == "__main__":
    print(json.dumps(timestamped_transcript(sys.argv[1])))
