def summarize_translation_quality(translations):
    issues = {}
    for original, translated in translations.items():
        if len(original) != len(translated):
            issues[original] = "Length mismatch"
    return issues
