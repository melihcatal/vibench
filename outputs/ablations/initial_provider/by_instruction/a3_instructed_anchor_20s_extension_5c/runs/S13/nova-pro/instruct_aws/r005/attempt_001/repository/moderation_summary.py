def moderation_summary(moderation_decisions):
    summary = 'Moderation Summary:'
    for decision in moderation_decisions:
        summary += f'\n- {decision}'
    return summary