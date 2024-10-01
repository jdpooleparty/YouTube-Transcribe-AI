import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import os
import textwrap
import time
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Function to extract YouTube video ID from a URL
def extract_youtube_id(url):
    # Check for different types of YouTube URLs
    regex_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',  # Standard YouTube URL
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',      # Embed URL
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)',          # /v/ URL
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',               # Shortened youtu.be URL
    ]
    
    for pattern in regex_patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)

    # If the URL contains additional parameters, extract the 'v' parameter value
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    
    return None

# Example YouTube URL
youtube_url = "https://www.youtube.com/watch?v=9uDpWfMbAdQ&list=PLG49S3nxzAnl_tQe3kvnmeMid0mjF8Le8&index=4"

# Extract the video ID from the URL
video_id = extract_youtube_id(youtube_url)
if video_id is None:
    print("Invalid YouTube URL")
else:
    # Retrieve transcript for the given YouTube video ID
    try:
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
        print(chunks)
        
    except Exception as e:
        print(f"An error occurred: {e}")
