def apply_safety_threshold(moderation_result, thresholds=None):
    thresholds = thresholds or {"TOXICITY": 0.7}
    
    for category, threshold_value in thresholds.items():
        if category in moderation_result and moderation_result[category] > threshold_value:
            return {"decision": "DENY", "reason": f"{category} score exceeds threshold"}
            
    return {"decision": "ALLOW", "reason": "All scores within thresholds"}
