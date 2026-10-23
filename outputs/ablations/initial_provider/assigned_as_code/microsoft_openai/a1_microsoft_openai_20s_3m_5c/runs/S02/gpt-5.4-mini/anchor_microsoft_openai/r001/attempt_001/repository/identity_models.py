def normalize_identity_claims(data):
    if not isinstance(data, dict):
        return {}
    return {
        'subject': data.get('sub') or data.get('id') or data.get('userPrincipalName') or data.get('mail'),
        'display_name': data.get('name') or data.get('displayName'),
        'email': data.get('email') or data.get('mail') or data.get('userPrincipalName'),
        'issuer': data.get('iss'),
        'tenant_id': data.get('tid'),
        'raw': data,
    }
