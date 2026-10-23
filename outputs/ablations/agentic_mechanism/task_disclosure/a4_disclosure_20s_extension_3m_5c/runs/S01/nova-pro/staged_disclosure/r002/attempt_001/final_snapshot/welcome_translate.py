import deepl

auth_key = 'YOUR_DEEPL_AUTH_KEY'
translator = deepl.Translator(auth_key)

onboarding_copy = 'Welcome to our service! We are glad to have you here.'
translated_copy = translator.translate_text(onboarding_copy, target_lang='DE')

print(translated_copy.text)