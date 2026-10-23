def partial_results(events):
    for event in events:
        if 'Transcript' in event:
            yield event['Transcript']