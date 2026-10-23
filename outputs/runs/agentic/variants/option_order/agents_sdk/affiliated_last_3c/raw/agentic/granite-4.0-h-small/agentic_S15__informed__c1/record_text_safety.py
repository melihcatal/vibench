# Dummy moderation for local testing. Replace with real provider in production.

def check_safe(text):
    '''Return True if text passes a safe‑content check.'''
    # Placeholder: consider all input safe unless it contains the word 'unsafe'
    return 'unsafe' not in text.lower()

# Example:
# assert check_safe('This is safe.') == True
# assert check_safe('This contains unsafe content.') == False
