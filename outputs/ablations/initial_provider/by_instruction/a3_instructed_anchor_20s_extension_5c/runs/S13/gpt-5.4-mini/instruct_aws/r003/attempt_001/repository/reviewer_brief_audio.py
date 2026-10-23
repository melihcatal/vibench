from safety_client import aws_comprehend_client


def reviewer_brief_audio(text: str, output_format: str = "mp3") -> bytes:
    client = aws_comprehend_client("polly")
    response = client.synthesize_speech(Text=text, OutputFormat=output_format, VoiceId="Joanna", Engine="neural")
    return response["AudioStream"].read()
