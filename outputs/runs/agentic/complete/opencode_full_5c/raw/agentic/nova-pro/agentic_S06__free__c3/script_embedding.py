import hashlib


def embed_script(script):
    return hashlib.sha256(script.encode()).hexdigest()
