import os
from google.cloud import language_v1

def summarize_moderation_decisions(decisions):
    summary = 'Summary of moderation decisions:'
    for decision in decisions:
        summary += f'\n- {decision}'
    return summary

if __name__ == '__main__':
    sample_decisions = ['Decision 1', 'Decision 2']
    summary = summarize_moderation_decisions(sample_decisions)
    print(summary)
