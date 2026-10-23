def secret_label_safety(payload):
    unsafe_keywords = ["password", "secret", "key", "credential", "token", "api_key", "connection_string"]
    unsafe_found = []

    labels = payload.get('labels', {})
    notes = payload.get('notes', "")
    secret_name = payload.get('secret_name', 'unknown')

    for key, value in labels.items():
        for keyword in unsafe_keywords:
            if keyword in key.lower() or keyword in value.lower():
                unsafe_found.append(f"Secret '{secret_name}': Unsafe keyword '{keyword}' found in label '{key}':'{value}'.")
    
    for keyword in unsafe_keywords:
        if keyword in notes.lower():
            unsafe_found.append(f"Secret '{secret_name}': Unsafe keyword '{keyword}' found in notes.")
            
    if not unsafe_found:
        return {'status': 'safe', 'message': f'Secret {secret_name}: No unsafe keywords found in labels or notes.'}
    else:
        return {'status': 'unsafe', 'message': f'Secret {secret_name}: Unsafe content detected.', 'details': unsafe_found}
