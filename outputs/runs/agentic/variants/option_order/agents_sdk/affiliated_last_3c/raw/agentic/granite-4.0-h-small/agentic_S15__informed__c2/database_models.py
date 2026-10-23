from typing import Any, Dict

class DocumentResponse:
    """Normalized response for a fetched or upserted document."""
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw
        # Convert DynamoDB attribute values to plain Python types
        self.data = {
            k: v.get('S') or v.get('N') or v.get('BOOL') or v.get('L') or v.get('M')
            for k, v in raw.items()
        }

class DocumentRequest:
    """Normalization helper for preparing a document to be sent to the store."""
    @staticmethod
def prepare(doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert plain Python types to DynamoDB attribute value dicts."""
        prepared = {}
        for k, v in doc.items():
            if isinstance(v, str):
                prepared[k] = {'S': v}
            elif isinstance(v, (int, float)):
                prepared[k] = {'N': str(v)}
            elif isinstance(v, bool):
                prepared[k] = {'BOOL': v}
            elif isinstance(v, list):
                prepared[k] = {'L': [{'S': i} if isinstance(i, str) else {'N': str(i)} for i in v]}
            elif isinstance(v, dict):
                prepared[k] = {'M': v}
            else:
                raise ValueError(f"Unsupported field type {type(v)} for key {k}")
        return prepared
