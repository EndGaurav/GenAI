from openai import OpenAI
client = OpenAI(
    api_key="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"
)

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)