import dashscope


# Summarize federated-login audit events
def summarize_audit_events(events):
    dashscope.api_key = os.environ["DASHSCOPE_API_KEY"]
    response = dashscope.Text.completions(
        model="qwen-turbo",
        prompt=f"Summarize the following audit events: {events}",
    )
    return response.choices[0].text
