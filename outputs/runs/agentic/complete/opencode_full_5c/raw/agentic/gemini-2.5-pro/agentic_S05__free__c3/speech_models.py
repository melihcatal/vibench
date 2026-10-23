from dataclasses import dataclass


@dataclass
class StreamingTranscript:
    transcript: str
    is_final: bool
    stability: float


def normalize_transcript_response(response):
    results = []
    for result in response.results:
        if not result.alternatives:
            continue

        alternative = result.alternatives[0]
        results.append(
            StreamingTranscript(
                transcript=alternative.transcript,
                is_final=result.is_final,
                stability=result.stability,
            )
        )
    return results
