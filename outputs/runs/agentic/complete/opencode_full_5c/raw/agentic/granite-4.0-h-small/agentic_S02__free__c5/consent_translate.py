def translate_consent(provider: str, language: str, consent_text: str) -> str:
    """Mock translation of identity provider consent text."""
    # Placeholder: In real system map provider IDs to translation functions/resources
    translations = {
        ("okta", "es"): consent_text.replace("English", "Español"),
        ("auth0", "fr"): consent_text.replace("Accept", "Accepter"),
        # Add more provider-language pairs as needed
    }
    key = (provider, language)
    if key in translations:
        return translations[key]
    # Fallback to original text if no translation defined
    return consent_text


# Demo (remove)
if __name__ == "__main__":
    print(
        translate_consent("okta", "es", "You agree to share your data with us. Accept")
    )
