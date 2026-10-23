# Placeholder for local request/response models if needed.
# For Google Secret Manager, the SDK objects are generally used directly.

class SecretValue:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"SecretValue(name='{self.name}', value='[REDACTED]')"

class ParsedJsonSecret:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data

    def __repr__(self):
        return f"ParsedJsonSecret(name='{self.name}', data={self.data})"
