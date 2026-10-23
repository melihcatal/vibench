import os
from google.cloud import kms_v1, logging_v2, contentsafety_v1beta, translate_v3
from openai import OpenAI

class SecurityClients:
    _kms_client = None
    _logging_client = None
    _content_safety_client = None
    _openai_client = None
    _translate_client = None

    @classmethod
    def get_kms_client(cls):
        if cls._kms_client is None:
            cls._kms_client = kms_v1.KeyManagementServiceClient()
        return cls._kms_client

    @classmethod
    def get_logging_client(cls):
        if cls._logging_client is None:
            cls._logging_client = logging_v2.LoggingServiceV2Client()
        return cls._logging_client

    @classmethod
    def get_content_safety_client(cls):
        if cls._content_safety_client is None:
            cls._content_safety_client = contentsafety_v1beta.ContentSafetyServiceClient()
        return cls._content_safety_client

    @classmethod
    def get_openai_client(cls):
        if cls._openai_client is None:
            cls._openai_client = OpenAI()
        return cls._openai_client

    @classmethod
    def get_translate_client(cls):
        if cls._translate_client is None:
            cls._translate_client = translate_v3.TranslationServiceClient()
        return cls._translate_client
