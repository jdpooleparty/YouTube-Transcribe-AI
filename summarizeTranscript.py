from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

import os
import textwrap
import re
import openai 


import time
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Retrieve OpenAI API credentials from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ORGANIZATION = os.getenv("OPENAI_ORGANIZATION")


# Ensure API key and organization ID are set
if not OPENAI_API_KEY or not OPENAI_ORGANIZATION:
    raise ValueError("Please set the OPENAI_API_KEY and OPENAI_ORGANIZATION environment variables")

# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization=OPENAI_ORGANIZATION)'
# openai.organization = OPENAI_ORGANIZATION

PROMPT_STRING = "Write a detailed summary of the following:\n\n<<SUMMARY>>\n"

# Retrieve transcript for the given YouTube video ID
video_id = "9uDpWfMbAdQ"
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

# Format the transcript using TextFormatter
formatter = TextFormatter()
transcript = formatter.format_transcript(transcript_list)

video_length = len(transcript)

# Adjust chunk size based on video length
chunk_size = 4000 if video_length >= 25000 else 2000

# Wrap the transcript in chunks
chunks = textwrap.wrap(transcript, chunk_size)

summaries = list()

# Retry logic for handling rate limits and errors
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_summary(chunk):
    prompt = PROMPT_STRING.replace("<<SUMMARY>>", chunk)

    # Using the new API method
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=256,
    temperature=0.7)
    return response.choices[0].message.content

# Generate summaries for each chunk
for idx, chunk in enumerate(chunks):
    try:
        summary = generate_summary(chunk)
        summary = re.sub(r"\s+", " ", summary.strip())
        summaries.append(summary)

        print(f"Processed chunk {idx+1}/{len(chunks)}")

        time.sleep(1)
    except Exception as e:
        print(f"Error processing chunk {idx+1}: {e}")
        continue

# Combine chunk summaries
chunk_summaries = " ".join(summaries)
prompt = PROMPT_STRING.replace("<<SUMMARY>>", chunk_summaries)

# Generate a final summary from the combined summaries
try:
    response = openai.chat.completions.create(model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=2048,
    temperature=0.7)
    final_summary = re.sub(r"\s+", " ", response.choices[0].message.content.strip())
except Exception as e:
    final_summary = "Could not generate the final summary due to an error."
    print(f"Error generating final summary: {e}")

# Print all summaries
for idx, summary in enumerate(summaries):
    print(f"({idx+1}) - {summary}\n")

print(f"(Final Summary) - {final_summary}")
