from typing import Iterable, List, Tuple

from speech_models import TranscriptSegment, segment_from_google_result


def handle_partial_and_final_results(results: Iterable[object]) -> Tuple[List[str], List[str]]:
    partials: List[str] = []
    finals: List[str] = []
    for result in results:
        segment: TranscriptSegment = segment_from_google_result(result)
        if not segment.text:
            continue
        if segment.is_final:
            finals.append(segment.text)
        else:
            partials.append(segment.text)
    return partials, finals
