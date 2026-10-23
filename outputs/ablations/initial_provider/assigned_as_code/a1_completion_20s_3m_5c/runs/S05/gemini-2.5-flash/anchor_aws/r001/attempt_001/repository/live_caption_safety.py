from googleapiclient import discovery
from typing import AsyncIterable

from speech_models import TranscriptSegment

async def live_caption_safety(transcript_segments: AsyncIterable[TranscriptSegment]):
    API_KEY = "YOUR_PERSPECTIVE_API_KEY" # Replace with your Perspective API Key
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    async for segment in transcript_segments:
        if segment.text:
            analyze_request = {
                'comment': {'text': segment.text},
                'requestedAttributes': {'TOXICITY': {}},
            }

            response = client.comments().analyze(body=analyze_request).execute()
            toxicity_score = response['attributeScores']['TOXICITY']['summaryScore']['value']

            is_unsafe = toxicity_score > 0.5 # Threshold for unsafe content, can be adjusted

            print(f"Transcript: '{segment.text}' | Toxicity Score: {toxicity_score:.2f} | Unsafe: {is_unsafe}")
            
            yield {
                "text": segment.text,
                "is_final": segment.is_final,
                "toxicity_score": toxicity_score,
                "is_unsafe": is_unsafe
            }
