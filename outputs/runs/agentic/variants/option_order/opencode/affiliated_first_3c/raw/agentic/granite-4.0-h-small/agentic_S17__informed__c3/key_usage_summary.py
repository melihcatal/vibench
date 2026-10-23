import os
from typing import Dict
from security_client import KeyManagementClient

class KeyUsageSummary:
    """Summarize key usage and crypto events via Key Management and Encryption service.",
    def __init__(self):
        self.client = KeyManagementClient()  # Uses AWS KMS as the concrete provider (identifiable by client implementation)

    def generate_summary(self) -> Dict[str, int]:
        """Fetch usage metrics and event counts, returning a summary dictionary.",
        usage = self.client.get_key_usage_metrics()
        summary = {
            'total_keys': usage['total_keys'],
            'encrypted_ops': usage['encrypt_ops'],
            'decrypted_ops': usage['decrypt_ops'],
            'errors': usage['error_count']
        }
        return summary
