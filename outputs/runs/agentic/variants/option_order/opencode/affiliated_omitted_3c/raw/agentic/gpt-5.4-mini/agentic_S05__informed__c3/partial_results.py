from speech_models import event_from_dict


def partial_results(events):
    for event in events:
        item = event_from_dict(event)
        if item.text:
            yield {"text": item.text, "final": item.is_final}
