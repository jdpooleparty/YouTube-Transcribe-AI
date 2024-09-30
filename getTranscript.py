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

# Check if API key and organization ID are set
if not OPENAI_API_KEY or not OPENAI_ORGANIZATION:
    raise ValueError("Please set the OPENAI_API_KEY and OPENAI_ORGANIZATION environment variables")

openai.organization = OPENAI_ORGANIZATION
openai.api_key = OPENAI_API_KEY

PROMPT_STRING = "Write a detailed summary of the following:\n\n<<SUMMARY>>\n"

# Retrieve transcript for a given YouTube video ID
video_id = "zzMLg3Ys5vI"
transcript = YouTubeTranscriptApi.get_transcript(video_id)

# Format the transcript using TextFormatter
formatter = TextFormatter()
transcript = formatter.format_transcript(transcript)

video_length = len(transcript)

# If the video is ~25 minutes or more, double the chunk size to reduce overall API calls
chunk_size = 4000 if video_length >= 25000 else 2000

# Wrap the transcript in chunks of characters
chunks = textwrap.wrap(transcript, chunk_size)

summaries = list()

# Retry logic to handle API rate limits and errors
@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_summary(chunk):
    prompt = PROMPT_STRING.replace("<<SUMMARY>>", chunk)
    
    # Using the new ChatCompletion with gpt-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.7  # You can adjust temperature as needed
    )
    return response['choices'][0]['message']['content']

# Generate summaries for each chunk
for chunk in chunks:
    try:
        # Generate summary using OpenAI API
        summary = generate_summary(chunk)
        summary = re.sub(r"\s+", " ", summary.strip())
        summaries.append(summary)
        
        # Sleep to avoid hitting rate limits (adjust as needed)
        time.sleep(1)
    except Exception as e:
        print(f"Error processing chunk: {e}")
        continue

# Join all the chunk summaries into one string
chunk_summaries = " ".join(summaries)
prompt = PROMPT_STRING.replace("<<SUMMARY>>", chunk_summaries)

# Generate a final summary from the chunk summaries
try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2056,
        temperature=0.7  # Adjust temperature as needed
    )
    final_summary = re.sub(r"\s+", " ", response['choices'][0]['message']['content'].strip())
except Exception as e:
    final_summary = "Could not generate the final summary due to an error."
    print(f"Error generating final summary: {e}")

# Print all the chunk summaries
for idx, summary in enumerate(summaries):
    print(f"({idx}) - {summary}\n")

print(f"(Final Summary) - {final_summary}")