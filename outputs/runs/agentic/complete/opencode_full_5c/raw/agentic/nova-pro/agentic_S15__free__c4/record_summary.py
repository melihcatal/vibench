def summarize_records(records):
    return [record.id for record in records]


if __name__ == "__main__":
    print(summarize_records([]))
