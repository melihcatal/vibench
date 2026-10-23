from security_client import create_kms_client, load_security_config
from security_models import encode_bytes, decode_bytes


def sign_or_verify_key(message: str, signature: str | None = None, key_id: str | None = None):
    config = load_security_config()
    client = create_kms_client(config)
    resolved_key_id = key_id or config.kms_key_id
    if signature is None:
        response = client.sign(KeyId=resolved_key_id, Message=message.encode('utf-8'), MessageType='RAW', SigningAlgorithm='RSASSA_PSS_SHA_256')
        return {'key_id': resolved_key_id, 'signature': encode_bytes(response['Signature'])}
    client.verify(KeyId=resolved_key_id, Message=message.encode('utf-8'), MessageType='RAW', Signature=decode_bytes(signature), SigningAlgorithm='RSASSA_PSS_SHA_256')
    return {'key_id': resolved_key_id, 'verified': True}
