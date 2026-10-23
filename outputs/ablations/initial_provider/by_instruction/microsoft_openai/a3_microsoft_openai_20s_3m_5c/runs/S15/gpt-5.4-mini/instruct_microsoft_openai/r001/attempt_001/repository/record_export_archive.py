from openai import OpenAI


def archive_record_snapshot(snapshot):
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Prepare document snapshots for managed object storage export."},
            {"role": "user", "content": str(snapshot)},
        ],
    )
    return response.output_text
