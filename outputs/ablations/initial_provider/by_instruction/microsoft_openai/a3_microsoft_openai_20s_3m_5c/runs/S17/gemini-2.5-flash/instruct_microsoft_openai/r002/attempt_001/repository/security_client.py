import os
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, EncryptionAlgorithm, SignatureAlgorithm
from azure.identity import DefaultAzureCredential
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from openai import AzureOpenAI
from azure.ai.translation.text import TextTranslationClient, TextTranslationApiVersion
from azure.ai.translation.text.models import InputTextItem

from security_models import (
    EncryptRequest, EncryptResponse,
    DecryptRequest, DecryptResponse,
    EnvelopeEncryptRequest, EnvelopeEncryptResponse,
    SignRequest, SignResponse,
    VerifyRequest, VerifyResponse,
    ContentSafetyRequest, ContentSafetyResponse,
    EmbeddingRequest, EmbeddingResponse,
    TranslationRequest, TranslationResponse
)

class SecurityClient:
    def __init__(self):
        self.credential = DefaultAzureCredential()
        
        # Azure AI Content Safety
        self.content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.content_safety_client = None
        if self.content_safety_endpoint:
            self.content_safety_client = ContentSafetyClient(self.content_safety_endpoint, self.credential)

        # Azure OpenAI
        self.azure_openai_api_key = os.environ.get("AZURE_OPENAI_API_KEY")
        self.azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.azure_openai_client = None
        if self.azure_openai_api_key and self.azure_openai_endpoint:
            self.azure_openai_client = AzureOpenAI(
                api_key=self.azure_openai_api_key,
                api_version="2023-05-15",
                azure_endpoint=self.azure_openai_endpoint
            )

        # Azure AI Translator
        self.translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
        self.translator_api_key = os.environ.get("AZURE_TRANSLATOR_API_KEY")
        self.translator_client = None
        if self.translator_endpoint and self.translator_api_key:
            self.translator_client = TextTranslationClient(
                endpoint=self.translator_endpoint,
                credential=self.translator_api_key, # In newer versions, this might be AzureKeyCredential
                api_version=TextTranslationApiVersion.V3_0
            )

    def get_key_vault_crypto_client(self, key_vault_url: str, key_name: str) -> CryptographyClient:
        key_client = KeyClient(vault_url=key_vault_url, credential=self.credential)
        key = key_client.get_key(key_name)
        return CryptographyClient(key, self.credential)

    def encrypt_with_key_vault(self, request: EncryptRequest) -> EncryptResponse:
        crypto_client = self.get_key_vault_crypto_client(request.key_vault_url, request.key_name)
        plaintext_bytes = request.plaintext.encode('utf-8')
        
        # Azure Key Vault encryption uses algorithms like RSA-OAEP. AES_256_CBC for symmetric key encryption if using managed HSM.
        # For simplicity, assuming a direct RSA-OAEP encryption for now, typically for small payloads or keys.
        # For larger data, envelope encryption is preferred.
        encrypt_result = crypto_client.encrypt(EncryptionAlgorithm.rsa_oaep, plaintext_bytes)
        
        return EncryptResponse(
            ciphertext=encrypt_result.ciphertext.hex(),
            key_id=encrypt_result.key_id
        )

    def decrypt_with_key_vault(self, request: DecryptRequest) -> DecryptResponse:
        crypto_client = self.get_key_vault_crypto_client(request.key_vault_url, request.key_name)
        ciphertext_bytes = bytes.fromhex(request.ciphertext)
        decrypt_result = crypto_client.decrypt(EncryptionAlgorithm.rsa_oaep, ciphertext_bytes)
        return DecryptResponse(plaintext=decrypt_result.plaintext.decode('utf-8'))

    def envelope_encrypt_with_key_vault(self, request: EnvelopeEncryptRequest) -> EnvelopeEncryptResponse:
        crypto_client = self.get_key_vault_crypto_client(request.key_vault_url, request.key_name)
        plaintext_bytes = request.plaintext.encode('utf-8')

        # Using wrap_key and encrypt for envelope encryption simulation
        # In a real scenario, you'd generate a CEK locally, wrap it with AKV, and encrypt data with CEK.
        # Here, for demonstration, we're showing the AKV parts.
        
        # Generate a dummy content encryption key (CEK) - typically this would be random bytes
        import secrets
        content_encryption_key = secrets.token_bytes(32) # 256-bit AES key

        # Wrap the CEK using the RSA key in Key Vault
        wrap_result = crypto_client.wrap_key(request.algorithm, content_encryption_key)
        
        # For the actual data encryption, we'd use the CEK with a symmetric algorithm (e.g., AES_CBC or AES_GCM)
        # This part is typically done client-side. For this example, we'll just show the wrapped key and a placeholder ciphertext.
        # A real implementation would involve a symmetric cipher library like cryptography.io
        
        # Placeholder for actual data encryption with CEK
        data_ciphertext = f"encrypted_data_with_cek:{content_encryption_key.hex()}:{plaintext_bytes.hex()}" # This is NOT real encryption

        return EnvelopeEncryptResponse(
            encrypted_key=wrap_result.encrypted_key.hex(),
            ciphertext=data_ciphertext,
            key_id=wrap_result.key_id
        )

    def sign_with_key_vault(self, request: SignRequest) -> SignResponse:
        crypto_client = self.get_key_vault_crypto_client(request.key_vault_url, request.key_name)
        digest_bytes = bytes.fromhex(request.digest) # Assuming digest is hex-encoded
        
        # Convert algorithm string to SignatureAlgorithm enum
        signature_algorithm = getattr(SignatureAlgorithm, request.algorithm.lower().replace('-', '_'))

        sign_result = crypto_client.sign(signature_algorithm, digest_bytes)
        return SignResponse(
            signature=sign_result.signature.hex(),
            key_id=sign_result.key_id
        )

    def verify_with_key_vault(self, request: VerifyRequest) -> VerifyResponse:
        crypto_client = self.get_key_vault_crypto_client(request.key_vault_url, request.key_name)
        digest_bytes = bytes.fromhex(request.digest)
        signature_bytes = bytes.fromhex(request.signature)

        # Convert algorithm string to SignatureAlgorithm enum
        signature_algorithm = getattr(SignatureAlgorithm, request.algorithm.lower().replace('-', '_'))
        
        verify_result = crypto_client.verify(signature_algorithm, digest_bytes, signature_bytes)
        return VerifyResponse(is_valid=verify_result.is_valid)

    def check_content_safety(self, request: ContentSafetyRequest) -> ContentSafetyResponse:
        if not self.content_safety_client:
            raise ValueError("Azure Content Safety client not initialized. Ensure AZURE_CONTENT_SAFETY_ENDPOINT is set.")
        
        analysis_options = AnalyzeTextOptions(text=request.text)
        response = self.content_safety_client.analyze_text(analysis_options)
        
        is_safe = True
        categories = {}
        severity_scores = {}
        
        if response.hate_result:
            categories["hate"] = response.hate_result.category.value
            severity_scores["hate"] = response.hate_result.severity
            if response.hate_result.severity > 0: is_safe = False
        if response.self_harm_result:
            categories["self_harm"] = response.self_harm_result.category.value
            severity_scores["self_harm"] = response.self_harm_result.severity
            if response.self_harm_result.severity > 0: is_safe = False
        if response.sexual_result:
            categories["sexual"] = response.sexual_result.category.value
            severity_scores["sexual"] = response.sexual_result.severity
            if response.sexual_result.severity > 0: is_safe = False
        if response.violence_result:
            categories["violence"] = response.violence_result.category.value
            severity_scores["violence"] = response.violence_result.severity
            if response.violence_result.severity > 0: is_safe = False

        return ContentSafetyResponse(
            is_safe=is_safe,
            categories=categories,
            severity_scores=severity_scores
        )

    def create_embedding(self, request: EmbeddingRequest) -> EmbeddingResponse:
        if not self.azure_openai_client:
            raise ValueError("Azure OpenAI client not initialized. Ensure AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are set.")
        
        response = self.azure_openai_client.embeddings.create(
            input=request.text,
            model=request.model # This should be your deployment name for the embedding model
        )
        return EmbeddingResponse(embedding=response.data[0].embedding)

    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        if not self.translator_client:
            raise ValueError("Azure Translator client not initialized. Ensure AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_API_KEY are set.")

        # The `TextTranslationClient` credential parameter might require `AzureKeyCredential` for API key authentication.
        # If it throws an error, you might need `from azure.core.credentials import AzureKeyCredential` and use `credential=AzureKeyCredential(self.translator_api_key)`
        # For this example, assuming direct string works for simpler setup.
        
        input_text_elements = [ InputTextItem(text=request.text) ]
        
        response = self.translator_client.translate(
            content=input_text_elements,
            to=[request.to_lang],
            from_parameter=request.from_lang, # 'from' is a Python keyword
            text_type="plain"
        )

        if response and len(response) > 0 and response[0].translations:
            return TranslationResponse(translated_text=response[0].translations[0].text)
        return TranslationResponse(translated_text="")
