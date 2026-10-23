"""
List or select a voice for a target locale using Amazon Polly.

This module provides voice discovery and selection functionality for
Amazon Polly, enabling locale-specific voice lookup and filtering
by gender, engine type, and language.

Provider: Amazon Polly (polly.us-east-1.amazonaws.com)
Voice IDs: Joanna, Matthew, Salli, Ivy, Kimberly, etc.
"""

from typing import List, Optional, Dict

from speech_client import PollyClient, get_polly_client
from speech_models import VoiceInfo, POLLY_VOICES, normalize_voice_id


def list_voices(
    language_code: Optional[str] = None,
    include_neural: bool = True,
    include_standard: bool = True,
    gender: Optional[str] = None,
    client: Optional[PollyClient] = None,
) -> List[VoiceInfo]:
    """
    List available Amazon Polly voices with optional filters.
    
    Args:
        language_code: BCP-47 language code (e.g., 'en-US', 'es-ES')
        include_neural: Include neural engine voices (NTTS)
        include_standard: Include standard engine voices
        gender: Filter by voice gender ('Female', 'Male')
        client: Optional pre-configured PollyClient
        
    Returns:
        List of VoiceInfo objects for matching voices
    """
    polly = client or get_polly_client()
    
    response = polly.describe_voices(language_code=language_code)
    voices_data = response.get("Voices", [])
    
    filtered_voices = []
    for voice_data in voices_data:
        engines = voice_data.get("SupportedEngines", [])
        
        # Filter by engine type
        if include_neural and include_standard:
            pass  # Include all
        elif include_neural and not include_standard:
            if "neural" not in engines:
                continue
        elif include_standard and not include_neural:
            if "standard" not in engines:
                continue
        else:
            continue  # Neither included
            
        # Filter by gender
        if gender and voice_data.get("Gender") != gender:
            continue
            
        filtered_voices.append(VoiceInfo.from_polly_response(voice_data))
    
    return filtered_voices


def select_voice_for_locale(
    locale: str = "en-US",
    gender: Optional[str] = None,
    prefer_neural: bool = True,
    client: Optional[PollyClient] = None,
) -> str:
    """
    Select the best Amazon Polly voice for a target locale.
    
    Args:
        locale: BCP-47 language code (e.g., 'en-US', 'es-ES', 'fr-FR')
        gender: Preferred voice spoker gender ('Female', 'Male')
        prefer_neural: Prefer neural (NTTS) voices over standard
        
    Returns:
        Selected Amazon Polly voice ID
    """
    # First check local voice mapping
    locale_voices = POLLY_VOICES.get(locale, [])
    
    if locale_voices:
        if gender:
            # Query Polly API to filter by gender
            voices = list_voices(
                language_code=locale,
                gender=gender,
                include_neural=prefer_neural,
                client=client,
            )
            if voices:
                return voices[0].voice_id
        
        # Return first voice for locale
        return locale_voices[0]
    
    # Fallback: query API for any voice in the language
    voices = list_voices(
        language_code=locale,
        include_neural=prefer_neural,
        gender=gender,
        client=client,
    )
    
    if voices:
        return voices[0].voice_id
    
    # Ultimate fallback to Joanna for English
    if locale.startswith("en"):
        return "Joanna"
    
    raise ValueError(f"No Amazon Polly voice found for locale: {locale}")


def get_voice_details(
    voice_id: str,
    client: Optional[PollyClient] = None,
) -> Optional[VoiceInfo]:
    """
    Get detailed information for a specific Amazon Polly voice.
    
    Args:
        voice_id: Amazon Polly voice ID (e.g., 'Joanna', 'Matthew')
        client: Optional pre-configured PollyClient
        
    Returns:
        VoiceInfo for the specified voice, or None if not found
    """
    polly = client or get_polly_client()
    
    # Polly doesn't have a get_voice endpoint, so we list and filter
    response = polly.describe_voices()
    voices = response.get("Voices", [])
    
    for voice_data in voices:
        if voice_data["Id"] == voice_id:
            return VoiceInfo.from_polly_response(voice_data)
    
    return None


def get_supported_locales() -> List[str]:
    """
    Get list of locales supported by Amazon Polly.
    
    Returns:
        List of BCP-47 language codes with available voices
    """
    return list(POLLY_VOICES.keys())


if __name__ == "__main__":
    # Example: List English US voices
    voices = list_voices(language_code="en-US")
    print(f"Found {len(voices)} voices for en-US:")
    for v in voices:
        print(f"  - {v.voice_id} ({v.gender}, engines: {v.supported_engines})")
    
    # Example: Select best voice for Spanish
    selected = select_voice_for_locale("es-ES", gender="Female")
    print(f"\nSelected voice for es-ES: {selected}")
