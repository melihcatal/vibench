from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse, Flag, Category, ThresholdConfig

def apply_category_thresholds(text: str, thresholds: ThresholdConfig) -> bool:
    """Apply per‑category severity thresholds to decide whether to allow the text.
    Returns True if the text passes all configured thresholds (i.e., is allowed).
    """
    client = SafetyClient()
    request = ModerationRequest(text=text)
    response: ModerationResponse = client.check_content(request)
    # Evaluate each category against its configured threshold
    for category, max_sev in thresholds.items():
        # Find the highest severity flag for this category
        max_flag_sev = Flag.NONE
        for flag in response.flags:
            if flag.category == category and flag.severity > max_flag_sev:
                max_flag_sev = flag.severity
        # If any category exceeds its allowed severity, reject the text
        if max_flag_sev > max_sev:
            return False
    return True

# Example usage (could be moved to a separate config file)
if __name__ == '__main__':
    cfg = ThresholdConfig(
        hate=Flag.WARNING,
        self_harm=Flag.WARNING,
        sexual=Flag.WARNING,
        violence=Flag.WARNING,
    )
    print(apply_category_thresholds('This is a harmless example.', cfg))
