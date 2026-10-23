from openai import OpenAI


client = OpenAI()


def main(text: str = "") -> dict:
    response = client.moderations.create(model="omni-moderation-latest", input=text)
    result = response.results[0]
    return {"flagged": result.flagged, "categories": dict(result.categories)}


if __name__ == "__main__":
    main()
