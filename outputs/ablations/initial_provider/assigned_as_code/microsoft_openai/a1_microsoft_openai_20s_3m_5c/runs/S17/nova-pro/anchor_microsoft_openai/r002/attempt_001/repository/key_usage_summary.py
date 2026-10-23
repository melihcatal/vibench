def summarize_key_usage(events):
    usage_summary = {}
    for event in events:
        if event['key_id'] not in usage_summary:
            usage_summary[event['key_id']] = {'encrypt_count': 0, 'decrypt_count': 0, 'sign_count': 0, 'verify_count': 0}
        if event['action'] == 'encrypt':
            usage_summary[event['key_id']]['encrypt_count'] += 1
        elif event['action'] == 'decrypt':
            usage_summary[event['key_id']]['decrypt_count'] += 1
        elif event['action'] == 'sign':
            usage_summary[event['key_id']]['sign_count'] += 1
        elif event['action'] == 'verify':
            usage_summary[event['key_id']]['verify_count'] += 1
    return usage_summary