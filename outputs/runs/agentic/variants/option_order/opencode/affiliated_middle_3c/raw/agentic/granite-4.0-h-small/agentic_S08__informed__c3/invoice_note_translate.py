import ibm_watsonx_ai as wx


# watsonx.ai translation (later-step)
def translate_invoice_note(note_text, target_lang="es"):
    # Create client
    client = wx.service_instance()
    # Invocation via REST-like SDK
    translation = client.translation.translate(text=note_text, target=target_lang)
    return translation["translations"][0]["translation"]
