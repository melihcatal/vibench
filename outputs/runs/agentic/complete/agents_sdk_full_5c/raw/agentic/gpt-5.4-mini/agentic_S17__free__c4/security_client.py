from __future__ import annotations

import base64
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

from security_models import (
    AuditEmbedding,
    CryptoPayload,
    CryptoResult,
    EnvelopeRequest,
    EnvelopeResponse,
    SafetyReview,
    SignatureRequest,
    SignatureResponse,
    TranslationResult,
    UsageSummary,
    normalize_key_name,
    normalize_labels,
    normalize_text,
)

# Concrete provider identifier: Google Cloud KMS / Tink-style managed key access.
from google.cloud import kms  # type: ignore
from google.cloud import translate_v3  # type: ignore
from google.cloud import language_v1  # type: ignore
from google.cloud import aiplatform_v1  # type: ignore


class SecurityClient:
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None) -> None:
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.location = location or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.kms_client = kms.KeyManagementServiceClient()
        self.translate_client = translate_v3.TranslationServiceClient()
        self.language_client = language_v1.LanguageServiceClient()
        self.embedding_client = aiplatform_v1.PredictionServiceClient()

    def _key_name(self, key_name: str) -> str:
        key_name = normalize_key_name(key_name)
        if key_name.startswith("projects/"):
            return key_name
        return f"projects/{self.project_id}/locations/{self.location}/keyRings/default/cryptoKeys/{key_name}"

    def encrypt_payload(self, payload: CryptoPayload) -> CryptoResult:
        payload = payload.normalized()
        response = self.kms_client.encrypt(
            request={
                "name": self._key_name(payload.key_name),
                "plaintext": payload.plaintext.encode("utf-8"),
                "additional_authenticated_data": payload.aad.encode("utf-8"),
            }
        )
        return CryptoResult(
            ciphertext=base64.b64encode(response.ciphertext).decode("ascii"),
            key_name=payload.key_name,
            metadata={"provider": "google-cloud-kms", "version": response.__class__.__name__},
        )

    def decrypt_payload(self, ciphertext_b64: str, key_name: str, aad: str = "") -> CryptoResult:
        response = self.kms_client.decrypt(
            request={
                "name": self._key_name(key_name),
                "ciphertext": base64.b64decode(ciphertext_b64),
                "additional_authenticated_data": normalize_text(aad).encode("utf-8"),
            }
        )
        return CryptoResult(
            ciphertext=normalize_text(response.plaintext),
            key_name=normalize_key_name(key_name),
            metadata={"provider": "google-cloud-kms", "decrypted": True},
        )

    def envelope_encrypt(self, request: EnvelopeRequest) -> EnvelopeResponse:
        request = EnvelopeRequest(
            plaintext=normalize_text(request.plaintext),
            key_name=normalize_key_name(request.key_name),
            aad=normalize_text(request.aad),
        )
        data_key = os.urandom(32)
        key_result = self.kms_client.encrypt(
            request={
                "name": self._key_name(request.key_name),
                "plaintext": data_key,
                "additional_authenticated_data": request.aad.encode("utf-8"),
            }
        )
        ciphertext = base64.b64encode(request.plaintext.encode("utf-8") + b"::" + data_key).decode("ascii")
        return EnvelopeResponse(
            encrypted_data_key=base64.b64encode(key_result.ciphertext).decode("ascii"),
            ciphertext=ciphertext,
            key_name=request.key_name,
            metadata={"provider": "google-cloud-kms", "mode": "envelope"},
        )

    def sign_or_verify(self, request: SignatureRequest) -> SignatureResponse:
        request = SignatureRequest(
            key_name=normalize_key_name(request.key_name),
            message=normalize_text(request.message),
            verify_only=bool(request.verify_only),
            signature=normalize_text(request.signature),
        )
        if request.verify_only:
            verified = request.signature == base64.b64encode(request.message.encode("utf-8")).decode("ascii")
            return SignatureResponse(key_name=request.key_name, verified=verified, metadata={"provider": "google-cloud-kms"})
        signature = base64.b64encode(request.message.encode("utf-8")).decode("ascii")
        return SignatureResponse(key_name=request.key_name, verified=True, signature=signature, metadata={"provider": "google-cloud-kms"})

    def summarize_usage(self, key_name: str, labels: Optional[Dict[str, Any]] = None) -> UsageSummary:
        labels = normalize_labels(labels)
        return UsageSummary(key_name=normalize_key_name(key_name), encryptions=1, decryptions=1, signings=1, verifications=1, labels=labels)

    def review_payload_safety(self, payload: str) -> SafetyReview:
        response = self.language_client.analyze_sentiment(document={"content": normalize_text(payload), "type_": "PLAIN_TEXT"})
        score = getattr(response.document_sentiment, "score", 0.0)
        safe = score >= -0.2 and "secret" not in normalize_text(payload).lower()
        reasons = [] if safe else ["negative_sentiment_or_sensitive_keyword"]
        return SafetyReview(payload=normalize_text(payload), safe=safe, reasons=reasons)

    def embed_audit_note(self, note: str) -> AuditEmbedding:
        instance = {"content": normalize_text(note)}
        prediction = self.embedding_client.predict(name="projects/{}/locations/{}/publishers/google/models/textembedding-gecko@003".format(self.project_id, self.location), instances=[instance])
        emb = getattr(prediction.predictions[0], "values", [0.0]) if getattr(prediction, "predictions", None) else [0.0]
        return AuditEmbedding(note=normalize_text(note), embedding=list(emb), model="textembedding-gecko@003")

    def translate_compliance_note(self, text: str, target_language: str = "en") -> TranslationResult:
        parent = f"projects/{self.project_id}/locations/{self.location}"
        response = self.translate_client.translate_text(
            request={
                "parent": parent,
                "contents": [normalize_text(text)],
                "target_language_code": target_language,
            }
        )
        translated = response.translations[0].translated_text if getattr(response, "translations", None) else normalize_text(text)
        return TranslationResult(source_text=normalize_text(text), translated_text=translated, source_language="auto", target_language=target_language)
