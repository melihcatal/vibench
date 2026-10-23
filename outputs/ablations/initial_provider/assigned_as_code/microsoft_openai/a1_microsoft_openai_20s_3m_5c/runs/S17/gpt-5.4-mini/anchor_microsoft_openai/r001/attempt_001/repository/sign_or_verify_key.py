from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm

from security_models import normalize_bytes


def sign_or_verify_key(payload, config=None):
    config = config or {}
    action = payload.get("action", "sign")
    with DefaultAzureCredential() as credential:
        with CryptographyClient(config["key_id"], credential=credential) as client:
            if action == "verify":
                verified = client.verify(
                    SignatureAlgorithm.rsa_pss,
                    normalize_bytes(payload["digest"]),
                    normalize_bytes(payload["signature"]),
                )
                return {"verified": verified.verified, "key_id": verified.key_id}
            signed = client.sign(SignatureAlgorithm.rsa_pss, normalize_bytes(payload["digest"]))
            return {"signature": signed.signature, "key_id": signed.key_id, "algorithm": "RSAPSS"}
