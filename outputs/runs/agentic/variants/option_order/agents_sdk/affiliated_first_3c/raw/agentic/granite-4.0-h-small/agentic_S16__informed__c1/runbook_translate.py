from rotation_summary import translate_runbook as _translate  # alias from rotation_summary module

# Wrapper that mimics a separate module
runbook_translate = _translate

# Demo usage
if __name__ == "__main__":
    sample = "Rotate API key and store the new value securely."
    print(runbook_translate(sample, target_lang='es'))