from azure.ai.contentsafety import (
    TextModerationOptions,
    HateTextCategory,
    SexualTextCategory,
    ViolenceTextCategory,
    SelfHarmTextCategory,
)

def get_text_moderation_options() -> TextModerationOptions:
    return TextModerationOptions(
        hate=HateTextCategory.Enabled,
        sexual=SexualTextCategory.Enabled,
        violence=ViolenceTextCategory.Enabled,
        self_harm=SelfHarmTextCategory.Enabled,
    )

def severity_to_score(severity: int) -> float:
    mapping = {0: 0.0, 2: 0.3, 4: 0.7, 6: 1.0}
    return mapping.get(severity, 1.0)

def parse_moderation_result(response) -> dict[str, float]:
    result = {}
    if hasattr(response, 'categories'):
        for cat_result in response.categories:
            cat_name = cat_result.category.name.lower()
            sev_val = getattr(cat_result.severity, 'value', int(cat_result.severity))
            result[cat_name] = severity_to_score(sev_val)
    return result
