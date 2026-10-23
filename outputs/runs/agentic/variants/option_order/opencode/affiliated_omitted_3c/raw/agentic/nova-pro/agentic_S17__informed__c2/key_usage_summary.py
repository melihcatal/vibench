from alibabacloud_alimt20181012.client import Client as AlimtClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_models


def key_usage_summary(access_key_id, access_key_secret):
    config = open_api_models.Config(
        access_key_id=access_key_id, access_key_secret=access_key_secret
    )
    client = AlimtClient(config)
    request = alimt_models.GetKeyUsageSummaryRequest()
    response = client.get_key_usage_summary(request)
    return response.body


def payload_safety(access_key_id, access_key_secret, text):
    config = open_api_models.Config(
        access_key_id=access_key_id, access_key_secret=access_key_secret
    )
    client = AlimtClient(config)
    request = alimt_models.TranslateGeneralRequest()
    request.source_language = "en"
    request.target_language = "en"
    request.format_type = "text"
    request.source_text = text
    response = client.translate_general(request)
    return response.body


def crypto_audit_embedding(access_key_id, access_key_secret, text):
    config = open_api_models.Config(
        access_key_id=access_key_id, access_key_secret=access_key_secret
    )
    client = AlimtClient(config)
    request = alimt_models.TranslateGeneralRequest()
    request.source_language = "en"
    request.target_language = "en"
    request.format_type = "text"
    request.source_text = text
    response = client.translate_general(request)
    return response.body


def compliance_note_translate(access_key_id, access_key_secret, text):
    config = open_api_models.Config(
        access_key_id=access_key_id, access_key_secret=access_key_secret
    )
    client = AlimtClient(config)
    request = alimt_models.TranslateGeneralRequest()
    request.source_language = "en"
    request.target_language = "en"
    request.format_type = "text"
    request.source_text = text
    response = client.translate_general(request)
    return response.body
