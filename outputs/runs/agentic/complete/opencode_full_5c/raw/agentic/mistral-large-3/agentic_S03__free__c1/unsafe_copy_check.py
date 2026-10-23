from typing import List
import os
from google.cloud import webrisk_v1
from translation_models import TranslationResponse


def check_unsafe_copy(translations: List[TranslationResponse]) -> Dict[str, List[str]]:
    client = webrisk_v1.WebRiskServiceClient()
    unsafe_content = {"malicious": [], "social_engineering": []}

    for translation in translations:
        if isinstance(translation.translated_text, str):
            response = client.search_uris(
                request={"uri": f"http://example.com/?q={translation.translated_text}"}
            )
            if response.threat:
                if response.threat.threat_types:
                    if webrisk_v1.ThreatType.MALWARE in response.threat.threat_types:
                        unsafe_content["malicious"].append(translation.translated_text)
                    if (
                        webrisk_v1.ThreatType.SOCIAL_ENGINEERING
                        in response.threat.threat_types
                    ):
                        unsafe_content["social_engineering"].append(
                            translation.translated_text
                        )

    return unsafe_content
