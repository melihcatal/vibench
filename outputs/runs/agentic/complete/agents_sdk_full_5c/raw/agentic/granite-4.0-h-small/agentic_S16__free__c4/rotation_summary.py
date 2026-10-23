# rotation_summary.py
# [LATER-STEP]
# Summarize secret rotation status using fetched rotation data
import json
from security_models import SecretRotationRequest, SecretRotationResponse, SecretFetchResponse
from security_client import get_secret_fetch_client, get_logger

logger = get_logger(__name__)

def summarize_rotation(request: SecretRotationRequest) -> SecretRotationResponse:
    """Read current and target versions, compare, and return a summary.",
    client = get_secret_fetch_client()
    try:
        current = client.read_secret_version(request['path'], version=request['current_version'])
        target = client.read_secret_version(request['path'], version=request['target_version'])
    except Exception as e:
        logger.error('Failed to read secret versions: %s', e)
        return {
            'path': request['path'],
            'version_requested': request['target_version'],
            'version_provided': request['current_version'],
            'success': False,
            'message': str(e),
        }
    summary = {
        'path': request['path'],
        'version_requested': request['target_version'],
        'version_provided': request['current_version'],
        'success': True,
        'message': 'Rotation successful',
    }
    # Simple diff of payloads (JSON-safe)
    try:
        cur_payload = json.loads(current['payload']) if isinstance(current['payload'], str) else current['payload']
        tgt_payload = json.loads(target['payload']) if isinstance(target['payload'], str) else target['payload']
        if cur_payload != tgt_payload:
            summary['message'] = 'Old and new payloads differ'
        else:
            summary['message'] = 'No change detected'
    except Exception:
        summary['message'] = 'Payload comparison not applicable'
    logger.info('Rotation summary: %s', summary)
    return summary

if __name__ == '__main__':
    req: SecretRotationRequest = {
        'path': 'my-database-credentials',
        'current_version': 'latest',
        'target_version': '2',
    }
    print(json.dumps(summarize_rotation(req), indent=2))
