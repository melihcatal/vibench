from typing import Iterable, List

from speech_models import event_from_result


def partial_results(results: Iterable[object], language_code: str = "en-US") -> List[str]:
    output = []
    for result in results:
        event = event_from_result(result, language_code)
        if event.text:
            output.append(event.text if event.is_final else event.text)
    return output
