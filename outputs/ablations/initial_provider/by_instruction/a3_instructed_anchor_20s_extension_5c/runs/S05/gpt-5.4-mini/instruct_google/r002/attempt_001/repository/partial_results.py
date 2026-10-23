from typing import Iterable, List

from speech_models import TranscriptSegment, normalize_transcript


def partial_and_final_results(results: Iterable[TranscriptSegment]) -> List[TranscriptSegment]:
    output: List[TranscriptSegment] = []
    for result in results:
        output.append(TranscriptSegment(text=normalize_transcript(result.text), is_final=result.is_final, confidence=result.confidence, language_code=result.language_code))
    return output
