def normalize_claims(claims):
    claims = claims or {}
    return {
        'subject': claims.get('sub') or claims.get('oid') or claims.get('id') or '',
        'email': claims.get('email') or claims.get('preferred_username') or claims.get('upn') or '',
        'display_name': claims.get('name') or claims.get('given_name') or claims.get('preferred_username') or '',
        'issuer': claims.get('iss') or '',
        'tenant_id': claims.get('tid') or '',
    }


def build_token_response(token_result):
    token_result = token_result or {}
    return {
        'access_token': token_result.get('access_token', ''),
        'refresh_token': token_result.get('refresh_token', ''),
        'id_token': token_result.get('id_token', ''),
        'expires_in': token_result.get('expires_in', 0),
        'scope': token_result.get('scope', ''),
    }
