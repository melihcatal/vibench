import json

# service: Microsoft Entra OIDC
# helper utilities for normalizing federated profile claims

NORMALIZED_FIELDS = {
    "sub": "user_id",
    "name": "display_name",
    "preferred_username": "email",
    "email": "email",
    "family_name": "last_name",
    "given_name": "first_name",
}


def normalize_profile(raw_profile):
    normalized = {}
    for key, mapped in NORMALIZED_FIELDS.items():
        if key in raw_profile:
            normalized[mapped] = raw_profile[key]
    return normalized


# Example raw profile from Microsoft Graph
# raw_profile = {
#     'id': '12345',
#     'displayName': 'John Doe',
#     'mail': 'john.doe@example.com',
#     'givenName': 'John',
#     'surname': 'Doe',
#     'userPrincipalName': 'john.doe@example.com'
# }

print(json.dumps(normalize_profile({"id": "123", "displayName": "Alice"}), indent=2))
