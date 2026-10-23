from typing import Iterable, Iterator

import boto3


def check_live_caption_safety(transcript_texts: Iterable[str]) -> Iterator[bool]:
    client = boto3.client("comprehend")
    for text in transcript_texts:
        response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode="en")
        segments = response.get("ResultList", [])
        yield any(segment.get("Toxicity", 0) > 0.5 for segment in segments)
