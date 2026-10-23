import os
import base64
from alibabacloud_ocr_api20210707.client import Client as OcrClient
from alibabacloud_tea_openapi.models import Config
from alibabacloud_ocr_api20210707 import models as ocr_models


ALIBABA_OCR_ENDPOINT = "ocr-api.cn-hangzhou.aliyuncs.com"
ALIBABA_OCR_REGION = "cn-hangzhou"


def get_ocr_config():
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set"
        )
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=ALIBABA_OCR_ENDPOINT,
        region_id=ALIBABA_OCR_REGION,
    )
    return config


def create_ocr_client():
    config = get_ocr_config()
    client = OcrClient(config)
    return client


def encode_image_to_base64(image_path=None, image_bytes=None):
    if image_bytes is not None:
        return base64.b64encode(image_bytes).decode("utf-8")
    if image_path is not None:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    raise ValueError("Either image_path or image_bytes must be provided")


def build_ocr_request(image_path=None, image_bytes=None):
    image_base64 = encode_image_to_base64(image_path, image_bytes)
    return ocr_models.RecognizeTextRequest(body=image_base64)


def build_advanced_ocr_request(image_path=None, image_bytes=None):
    image_base64 = encode_image_to_base64(image_path, image_bytes)
    return ocr_models.RecognizeAdvancedRequest(body=image_base64)


def build_table_ocr_request(image_path=None, image_bytes=None):
    image_base64 = encode_image_to_base64(image_path, image_bytes)
    return ocr_models.RecognizeTableRequest(body=image_base64)


def build_key_value_ocr_request(image_path=None, image_bytes=None):
    image_base64 = encode_image_to_base64(image_path, image_bytes)
    return ocr_models.RecognizeKeyValuesRequest(body=image_base64)
