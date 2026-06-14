import os
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"]
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "Explain Kafka consumer lag in 3 bullet points."
        }
    ]
)

print(message.content[0].text)