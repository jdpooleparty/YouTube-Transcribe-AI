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

# Function to copy transcript to clipboard
def copy_transcript():
    transcript_textbox.config(state=tk.NORMAL)  # Enable editing temporarily to copy text
    transcript = transcript_textbox.get("1.0", tk.END).strip()  # Retrieve all text from the textbox
    if transcript:
        root.clipboard_clear()  # Clear clipboard
        root.clipboard_append(transcript)  # Append transcript to clipboard
        root.update()  # Now it stays on the clipboard even after the window is closed
    else:
        messagebox.showwarning("Warning", "No transcript available to copy.")
    transcript_textbox.config(state=tk.DISABLED)  # Disable editing again

# Set up the main application window
root = tk.Tk()
root.title("YouTube Transcript Getter")
root.geometry("750x550")
root.configure(bg="#e0f7fa")  # Light blue background

# Example: Applying Variation 1
LABEL_STYLE = {'bg': '#d0e7ff', 'fg': 'black', 'font': ('Arial', 12, 'bold')}
ENTRY_STYLE = {'highlightbackground': '#000000', 'highlightthickness': 2, 'bg': '#f0f8ff', 'fg': 'black'}
BUTTON_STYLE = {'bg': '#005b96', 'fg': 'white', 'activebackground': '#03396c', 'font': ('Arial', 11, 'bold')}
TEXTBOX_STYLE = {'bg': '#f0f8ff', 'fg': 'black', 'highlightbackground': '#000000', 'highlightthickness': 2}


# YouTube URL Label and Entry
tk.Label(root, text="YouTube URL:", **LABEL_STYLE).pack(pady=5)
url_entry = tk.Entry(root, width=60, **ENTRY_STYLE)
url_entry.pack(pady=5)

# Retrieve Transcript Button
retrieve_button = tk.Button(root, text="Get Transcript", command=retrieve_transcript, **BUTTON_STYLE)
retrieve_button.pack(pady=10)

# ScrolledText Widget to Display the Transcript
transcript_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, state=tk.DISABLED, **TEXTBOX_STYLE)
transcript_textbox.pack(pady=10)

# Copy Transcript Button
copy_button = tk.Button(root, text="Copy Transcript", command=copy_transcript, **BUTTON_STYLE)
copy_button.pack(pady=10)

# Set the focus to the URL entry field when the application starts
url_entry.focus()

# Run the GUI event loop
root.mainloop()
