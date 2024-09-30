import openai
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print(client)


# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=os.getenv("OPENAI_ORGANIZATION"))'
# openai.organization = os.getenv("OPENAI_ORGANIZATION")

response = client.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": "Hello, how are you?"}],
max_tokens=50)

print((response.choices[0].message.content)['content'])