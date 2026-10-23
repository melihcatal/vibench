def safety_threshold(payload, config=None):
    config = config or {}
    thresholds = config.get('thresholds', {})
    
    # Example payload: {'toxicity': 0.8}
    moderation_score = payload.get('toxicity', 0.0)
    
    # Default threshold for toxicity if not provided in config
    toxicity_threshold = thresholds.get('toxicity', 0.5)
    
    if moderation_score > toxicity_threshold:
        return {'decision': 'deny', 'reason': f'Toxicity score {moderation_score} exceeds threshold {toxicity_threshold}'}
    else:
        return {'decision': 'allow', 'reason': f'Toxicity score {moderation_score} is within threshold {toxicity_threshold}'}