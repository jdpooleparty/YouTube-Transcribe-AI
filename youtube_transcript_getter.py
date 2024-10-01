import re
import textwrap
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Function to extract YouTube video ID from a URL
def extract_youtube_id(url):
    regex_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',  
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',     
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)',         
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',              
    ]
    
    for pattern in regex_patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)

    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query).get('v')
    if video_id:
        return video_id[0]
    
    return None

# Function to retrieve and display the transcript
def retrieve_transcript():
    youtube_url = url_entry.get()

    # Extract the video ID from the URL
    video_id = extract_youtube_id(youtube_url)
    if video_id is None:
        messagebox.showerror("Error", "Invalid YouTube URL")
    else:
        try:
            # Retrieve transcript for the given YouTube video ID
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Format the transcript using TextFormatter
            formatter = TextFormatter()
            transcript = formatter.format_transcript(transcript_list)
            
            # Adjust chunk size based on video length
            video_length = len(transcript)
            chunk_size = 4000 if video_length >= 25000 else 2000
            chunks = textwrap.wrap(transcript, chunk_size)
            
            # Display the transcript in the text area
            transcript_textbox.config(state=tk.NORMAL)  # Enable editing
            transcript_textbox.delete(1.0, tk.END)  # Clear the text area
            for chunk in chunks:
                transcript_textbox.insert(tk.END, chunk + "\n\n")
            transcript_textbox.config(state=tk.DISABLED)  # Disable editing
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main application window
root = tk.Tk()
root.title("YouTube Transcript Getter")
root.geometry("700x500")

# YouTube URL Label and Entry
tk.Label(root, text="YouTube URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(pady=5)

# Retrieve Transcript Button
retrieve_button = tk.Button(root, text="Get Transcript", command=retrieve_transcript)
retrieve_button.pack(pady=10)

# ScrolledText Widget to Display the Transcript
transcript_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED)
transcript_textbox.pack(pady=10)

# Run the GUI event loop
root.mainloop()
