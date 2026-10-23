# security_models.py
# [HELPER]
# Define local request, response, and normalization helpers for Secret Management
from typing import TypedDict, Any, Dict, List

# Request models

class SecretFetchRequest(TypedDict):
    name: str
    version: int | str = ...  # latest version can be 'latest' or a number
    provider: str | None = None  # optional hint if caller wants explicit provider

class SecretLabelSafetyRequest(TypedDict):
    secret_id: str
    labels: Dict[str, str]
    notes: str | None = None

class SecretRotationRequest(TypedDict):
    path: str  # Vault path or AWS secret name etc.
    target_version: int | str
    current_version: int | str

class SecretAuditNote(TypedDict):
    id: str
    title: str
    description: str
    severity: str  # e.g., 'INFO', 'WARN', 'ERROR'
    metadata: Dict[str, Any] = ...

class SecretAuditNoteList(TypedDict):
    notes: List[SecretAuditNote]

# Response models (normalized)

class SecretFetchResponse(TypedDict):
    secret_id: str
    payload: Any  # raw secret value (string, json dict, etc.)
    version: int | str
    provider: str

class SecretLabelSafetyResponse(TypedDict):
    secret_id: str
    unsafe: bool
    details: List[str]  # list of offending labels/notes

class SecretRotationResponse(TypedDict):
    path: str
    version_requested: int | str
    version_provided: int | str
    success: bool
    message: str

class SecretAuditEmbeddingResponse(TypedDict):
    id: str
    embedding: List[float]
    source_note_ids: List[str]

# Example normalization helper (can be expanded)

def normalize_secret_response(raw: Dict[str, Any], provider: str) -> SecretFetchResponse:
    if provider == 'aws':
        # AWS Secrets Manager response structure
        return {
            'secret_id': raw['Name'],
            'payload': raw['SecretString'] if raw.get('SecretString') else json.loads(raw['SecretBinary']),
            'version': raw.get('VersionId', 'latest'),
            'provider': 'aws',
        }
    elif provider == 'azure':
        # Placeholder for Azure Key Vault response; adapt as needed
        return {
            'secret_id': raw.get('id'),
            'payload': raw.get('value'),
            'version': raw.get('attributes', {}).get('updated'),
            'provider': 'azure',
        }
    elif provider == 'gcp':
        # GCP Secret Manager response
        return {
            'secret_id': raw['name'],
            'payload': json.loads(raw['payload']['data']),
            'version': raw['name'].rsplit('/', maxsplit=1)[-1],
            'provider': 'gcp',
        }
    raise ValueError('Unsupported provider')

# Simple unsafe label/notes detector (case‑insensitive keyword list)
UNSAFE_KEYWORDS = {'password', 'secret', 'apikey', 'credential'}

def check_secret_labels(request: SecretLabelSafetyRequest) -> SecretLabelSafetyResponse:
    unsafe_items = []
    # Scan labels
    for label, value in request.get('labels', {}).items():
        lowered = value.lower()
        for kw in UNSAFE_KEYWORDS:
            if kw in lowered:
                unsafe_items.append(f'Label {label} contains "{kw}"')
    # Scan notes
    notes = request.get('notes', '')
    for kw in UNSAFE_KEYWORDS:
        if kw.lower() in notes.lower():
            unsafe_items.append(f'Notes contain "{kw}"')
    return {
        'secret_id': request['secret_id'],
        'unsafe': bool(unsafe_items),
        'details': unsafe_items,
    }

# End of module
