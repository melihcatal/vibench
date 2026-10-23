from typing import Dict, Iterable, List

from speech_models import StreamingCaption, captions_from_events


def partial_results(events: Iterable[Dict[str, object]]) -> List[StreamingCaption]:
    return captions_from_events(list(events))
