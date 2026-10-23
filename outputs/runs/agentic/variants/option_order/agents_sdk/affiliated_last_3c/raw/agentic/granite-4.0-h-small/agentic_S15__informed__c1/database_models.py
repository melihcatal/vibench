import json, hashlib


def generate_etag(file_path):
    '''Compute the ETag (MD5) of a local file for S3 upload verification.'''
    buf_size = 65536
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(buf_size), b" "):
            md5.update(chunk)
    return md5.hexdigest()

# Usage example (local):
# etag = generate_etag('exports/my_snapshot.json')
