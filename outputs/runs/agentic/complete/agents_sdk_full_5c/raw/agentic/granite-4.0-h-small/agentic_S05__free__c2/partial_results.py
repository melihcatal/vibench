def handle_event(event):
    """Processes a single streaming recognition event.
    Args:
        event (dict): JSON payload containing 'results' with 'alternatives'.
    Returns:
        bool: True if this is a final result, False otherwise.
    """    results = event.get('results', [])
    for result in results:
        alternatives = result.get('alternatives', [])
        if alternatives and alternatives[0].get('transcript'):
            transcript = alternatives[0]['transcript']
            is_final = result.get('is_final', False)
            print('Transcript:', transcript, '| Final:', is_final)
            return is_final
    return False