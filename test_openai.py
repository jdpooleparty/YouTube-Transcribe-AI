import openai
import os

# Set up the API key and organization
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=os.getenv("OPENAI_ORGANIZATION"))'
# openai.organization = os.getenv("OPENAI_ORGANIZATION")

response = openai.chat.completions.create(model="gpt-3.5-turbo",
messages=[{"role": "user", "content": "Hello, how are you?"}],
max_tokens=50)

print(response.choices[0].message.content)