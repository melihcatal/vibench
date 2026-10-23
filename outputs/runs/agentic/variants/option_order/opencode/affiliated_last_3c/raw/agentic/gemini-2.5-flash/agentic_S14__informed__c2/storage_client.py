import os
from google.cloud import (
    storage,
    documentai_v1beta3 as documentai,
    translate_v3 as translate,
)
import google.generativeai as genai


class StorageClient:
    _storage_client = None
    _documentai_client = None
    _translate_client = None
    _generative_model_client = None

    @classmethod
    def get_storage_client(cls):
        if cls._storage_client is None:
            cls._storage_client = storage.Client()
        return cls._storage_client

    @classmethod
    def get_documentai_client(cls):
        if cls._documentai_client is None:
            cls._documentai_client = documentai.DocumentProcessorServiceClient()
        return cls._documentai_client

    @classmethod
    def get_translate_client(cls):
        if cls._translate_client is None:
            cls._translate_client = translate.TranslationServiceClient()
        return cls._translate_client

    @classmethod
    def get_generative_model_client(cls):
        if cls._generative_model_client is None:
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set.")
            genai.configure(api_key=api_key)
            cls._generative_model_client = genai
        return cls._generative_model_client
