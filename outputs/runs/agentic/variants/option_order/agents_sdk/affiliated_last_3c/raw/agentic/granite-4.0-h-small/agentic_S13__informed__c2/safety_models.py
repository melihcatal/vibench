from typing import TypedDict

# -------------------------------------------------
# Normalized request / response models for the
# same‑scenario safety step
# -------------------------------------------------
ModSafetyRequest = TypedDict('ModSafetyRequest', {
    'text': str,
    'options': dict,
})
ModSafetyResponse = TypedDict('ModSafetyResponse', {
    'provider': str,
    'raw_response': dict,
})

# Export for later‑step scripts
__all__ = ['ModSafetyRequest', 'ModSafetyResponse']
