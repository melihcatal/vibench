# [LATER-STEP] localized_platform_output.py
# Translate watsonx.ai model output to a target locale using IBM Translation service

import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from typing import Dict, Any
from model_models import NormalizedResponse
from dataclasses import dataclass


@dataclass
class LocalizationRequest:
    output_text: str
    target_locale: str = "es"  # default Spanish; change as needed


def localize(
    output: NormalizedResponse, target_locale: str = "es"
) -> NormalizedResponse:
    """Translate the generated text to the requested locale and preserve metadata."""
    api_key = os.getenv("WATSONX_API_KEY")
    service_url = os.getenv(
        "WATSONX_SERVICE_URL"
    )  # e.g., https://us-south.language-translator.watson.cloud.ibm.com
    if not api_key or not service_url:
        raise RuntimeError(
            "Set WATSONX_API_KEY and WATSONX_SERVICE_URL environment variables"
        )

    authenticator = IAMAuthenticator(api_key)
    translator = LanguageTranslatorV3(
        version="2022-03-30",
        url=service_url,
        authenticator=authenticator,
    )
    translator.set_disable_ssl_verification(True)  # for local testing; remove in prod

    # Translate using the 'translate_text' endpoint
    translation = translator.translate_text(
        text=[output.output_text],
        model_id="en-" + target_locale,
        source="en",
        target=target_locale,
    ).get_result()

    translated_text = translation["translations"][0]["translation"]
    # Build new normalized response preserving original metadata
    new_metadata = output.request_metadata.copy()
    new_metadata["translation_locale"] = target_locale
    return NormalizedResponse(
        output_text=translated_text,
        raw_response=translation,
        request_metadata=new_metadata,
    )
