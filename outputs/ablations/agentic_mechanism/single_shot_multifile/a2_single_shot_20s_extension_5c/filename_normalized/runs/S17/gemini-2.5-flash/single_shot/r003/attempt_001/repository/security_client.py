import os
import boto3
from openai import OpenAI
from google.cloud import dlp_v2
from google.cloud import translate_v3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

def get_aws_region() -> str:
    return os.environ.get("AWS_REGION", "us-east-1")

def get_gcp_project_id() -> str:
    return os.environ.get("GCP_PROJECT_ID")

def get_kms_client():
    return boto3.client("kms", region_name=get_aws_region())

def get_cloudtrail_client():
    return boto3.client("cloudtrail", region_name=get_aws_region())

def get_dlp_client():
    return dlp_v2.DlpServiceClient()

def get_openai_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_translate_client():
    return translate_v3.TranslationServiceClient()

def local_aes_gcm_encrypt(plaintext: bytes, key: bytes):
    if len(key) != 32:
        raise ValueError("AES key must be 32 bytes for AES-256")

    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return ciphertext, iv, encryptor.tag

def local_aes_gcm_decrypt(ciphertext: bytes, key: bytes, iv: bytes, tag: bytes):
    if len(key) != 32:
        raise ValueError("AES key must be 32 bytes for AES-256")

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext

def encode_bytes_to_b64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')

def decode_b64_to_bytes(data: str) -> bytes:
    return base64.b64decode(data)
