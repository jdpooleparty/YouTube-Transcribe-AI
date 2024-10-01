import re
from urllib.parse import urlparse, parse_qs

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

# Example usage
youtube_url = "https://www.youtube.com/watch?v=9uDpWfMbAdQ&list=PLG49S3nxzAnl_tQe3kvnmeMid0mjF8Le8&index=4"
video_id = extract_youtube_id(youtube_url)
print(f"Video ID: {video_id}")