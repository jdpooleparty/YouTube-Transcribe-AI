import re
import textwrap
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

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

# Function to display the selected prompt
def display_prompt(event):
    selected_item = prompt_treeview.focus()
    if selected_item:
        item_data = prompt_treeview.item(selected_item)
        if 'values' in item_data and item_data['values']:
            prompt_text = item_data['values'][0]
            prompt_textbox.config(state=tk.NORMAL)
            prompt_textbox.delete(1.0, tk.END)
            prompt_textbox.insert(tk.END, prompt_text)
            prompt_textbox.config(state=tk.DISABLED)
        else:
            prompt_textbox.config(state=tk.NORMAL)
            prompt_textbox.delete(1.0, tk.END)
            prompt_textbox.config(state=tk.DISABLED)

# Function to copy selected GPT prompt to clipboard
def copy_prompt():
    prompt_textbox.config(state=tk.NORMAL)
    selected_prompt = prompt_textbox.get("1.0", tk.END).strip()
    prompt_textbox.config(state=tk.DISABLED)
    if selected_prompt:
        if include_transcript_var.get():
            transcript_textbox.config(state=tk.NORMAL)
            transcript = transcript_textbox.get("1.0", tk.END).strip()
            transcript_textbox.config(state=tk.DISABLED)
            full_text = f"{selected_prompt}\n\n{transcript}"
        else:
            full_text = selected_prompt
        root.clipboard_clear()
        root.clipboard_append(full_text)
        root.update()
    else:
        messagebox.showwarning("Warning", "Please select a prompt to copy.")

# Set up the main application window
root = tk.Tk()
root.title("YouTube Transcribe AI")
root.geometry("850x900")

# Define colors and fonts for styling
BG_COLOR = '#BBDEFB'  # Even lighter blue background
FONT_COLOR = '#000000'  # Black font color for better contrast
TRIM_COLOR = '#000000'  # Black trim
default_font = ('Segoe UI', 12)

root.configure(bg=BG_COLOR)
root.option_add("*Font", default_font)

# Configure styles
style = ttk.Style()
style.theme_use('clam')

# Set styles for different widgets
style.configure('TLabel', background=BG_COLOR, foreground=FONT_COLOR)
style.configure('TFrame', background=BG_COLOR)
style.configure('TButton', background='#1565C0', foreground='#FFFFFF', font=('Segoe UI', 11, 'bold'))
style.map('TButton', background=[('active', '#1E88E5')])
style.configure('TCheckbutton', background=BG_COLOR, foreground=FONT_COLOR)
style.map('TCheckbutton', background=[('active', BG_COLOR)], foreground=[('active', FONT_COLOR)])
style.configure('TLabelframe', background=BG_COLOR, foreground=FONT_COLOR, bordercolor=TRIM_COLOR)
style.configure('TLabelframe.Label', background=BG_COLOR, foreground=FONT_COLOR)

# Set up the main frame
main_frame = ttk.Frame(root, padding="10 10 10 10", style='TFrame')
main_frame.pack(fill='both', expand=True)

main_frame.columnconfigure(0, weight=0)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(2, weight=1)

# YouTube URL Label and Entry
url_label = ttk.Label(main_frame, text="YouTube URL:")
url_label.grid(row=0, column=0, sticky='W', padx=5, pady=5)
url_entry = ttk.Entry(main_frame, width=70)
url_entry.grid(row=0, column=1, sticky='EW', padx=5, pady=5)

# Retrieve Transcript Button
retrieve_button = ttk.Button(main_frame, text="Get Transcript", command=retrieve_transcript)
retrieve_button.grid(row=1, column=0, columnspan=2, pady=10)

# ScrolledText Widget to Display the Transcript
transcript_frame = ttk.Frame(main_frame)
transcript_frame.grid(row=2, column=0, columnspan=2, sticky='NSEW', padx=5, pady=5)
transcript_frame.columnconfigure(0, weight=1)
transcript_frame.rowconfigure(0, weight=1)

transcript_textbox = scrolledtext.ScrolledText(
    transcript_frame, wrap=tk.WORD, width=80, height=15, state=tk.DISABLED,
    bg='#FFFFFF', fg='#000000', highlightbackground=TRIM_COLOR, highlightthickness=1,
    borderwidth=1, relief='solid'
)
transcript_textbox.grid(row=0, column=0, sticky='NSEW')

transcript_textbox.configure(font=('Segoe UI', 12))

# Copy Transcript Button
copy_button = ttk.Button(main_frame, text="Copy Transcript", command=copy_transcript)
copy_button.grid(row=3, column=0, columnspan=2, pady=10)

# GPT Prompts Section
prompts_by_category = {
    "1. Focus on Understanding and Application": [
        ("Explain key concepts to a beginner", "As you review this transcript, explain the key concepts as if you were teaching them to a beginner. Provide examples, analogies, and practical applications that make the ideas easy to grasp and remember."),
        ("Transform into step-by-step guide", "Transform this transcript into a step-by-step guide that I can follow. Highlight the main points, but also include action items and exercises I can do to apply this knowledge in real life.")
    ],
    "2. Emphasize Key Takeaways and Memory Aids": [
        ("Create mnemonic or visual metaphor", "From this transcript, identify the most critical points and create a mnemonic, acronym, or visual metaphor to help me retain the information."),
        ("Prepare me for a quiz", "Explain the concepts from this transcript as if you were preparing me for a quiz. Ask me questions along the way and then provide detailed answers.")
    ],
    "3. Connect Concepts with Prior Knowledge": [
        ("Relate ideas to prior knowledge", "Relate the ideas from this transcript to something I might already know. How do these concepts connect with other subjects, fields, or experiences?"),
        ("Compare with other disciplines", "Compare the key points from this transcript with concepts from other disciplines or real-world examples. Show me how they are similar or different.")
    ],
    "4. Deep-Dive Analysis and Insight": [
        ("Provide advanced lecture", "Pretend you're a university professor giving an advanced lecture on this topic. Go beyond the transcript, provide deeper insights, historical context, and why these ideas are significant today."),
        ("Critical analysis of arguments", "Dissect the arguments or points made in this transcript. What are the strengths, weaknesses, and potential counterarguments? Provide a critical analysis.")
    ],
    "5. Personalization and Engagement": [
        ("Teach as a personal tutor", "Teach me the ideas from this transcript as if you were a personal tutor who knows my learning style. Use humor, storytelling, or interactive examples to keep me engaged."),
        ("Include reflective questions", "Summarize the transcript, but include reflective questions that make me think about how I can apply this knowledge to my own life or work.")
    ],
    "6. Visualization and Demonstration": [
        ("Create a mental picture", "Create a mental picture or visual representation of the key points in this transcript. Describe it in vivid detail so that I can 'see' the concepts in my mind."),
        ("Simulate real-world scenario", "Simulate a real-world scenario where I would use the information from this transcript. Walk me through how I would apply these concepts step-by-step.")
    ],
    "7. Storytelling and Analogies": [
        ("Turn key points into a story", "Turn the key points from this transcript into a story, with characters, a plot, and a conclusion that ties all the concepts together."),
        ("Use analogies for explanation", "Use analogies to explain the ideas in this transcript. Compare them to everyday objects, events, or experiences so I can easily understand and remember them.")
    ],
    "8. Collaborative Learning and Problem-Solving": [
        ("Act as my study partner", "Act as my study partner. Break down the transcript into discussion points and ask me questions as if we're preparing for an exam together."),
        ("Identify and solve a problem", "From the transcript, identify a problem or challenge related to the topic. Help me brainstorm solutions and guide me through the thought process.")
    ],
    "9. Multiple Perspectives and Debate": [
        ("Explain from different perspectives", "Explain the concepts from different perspectives (e.g., a beginner, an expert, a child, or a skeptic). Show how the understanding changes based on each viewpoint."),
        ("Play devil's advocate", "Play devil's advocate for this transcript. Challenge the ideas presented, and then defend them, helping me see both sides of the argument.")
    ],
    "10. Retention and Reinforcement Techniques": [
        ("Create questions or flashcards", "After explaining this transcript, create a series of questions, flashcards, or mini-quizzes to test my understanding and reinforce the learning."),
        ("Summarize as a TED Talk", "Summarize this transcript as if you're preparing it for a TED Talk, focusing on the most impactful and memorable points that will leave a lasting impression.")
    ]
}

prompt_frame = ttk.LabelFrame(main_frame, text="GPT Prompts", style='TLabelframe')
prompt_frame.grid(row=4, column=0, columnspan=2, sticky='NSEW', padx=5, pady=10)
prompt_frame.columnconfigure(0, weight=1)
prompt_frame.rowconfigure(1, weight=1)

# Treeview to display categories and prompts
prompt_treeview = ttk.Treeview(prompt_frame)
prompt_treeview.heading('#0', text='Select a Prompt', anchor='w')
prompt_treeview.column('#0', stretch=True)
prompt_treeview.grid(row=1, column=0, sticky='NSEW', padx=5, pady=5)
prompt_treeview.bind('<<TreeviewSelect>>', display_prompt)

# Scrollbar for the Treeview
treeview_scrollbar = ttk.Scrollbar(prompt_frame, orient=tk.VERTICAL, command=prompt_treeview.yview)
prompt_treeview.configure(yscrollcommand=treeview_scrollbar.set)
treeview_scrollbar.grid(row=1, column=1, sticky='NS')

# Populate the Treeview
for category, prompts in prompts_by_category.items():
    category_id = prompt_treeview.insert('', 'end', text=category, open=False)
    for title, prompt in prompts:
        prompt_treeview.insert(category_id, 'end', text=title, values=(prompt,))

# Text widget to display the selected prompt with word wrap
prompt_textbox = scrolledtext.ScrolledText(
    prompt_frame, wrap=tk.WORD, width=80, height=8, state=tk.DISABLED,
    bg='#FFFFFF', fg='#000000', highlightbackground=TRIM_COLOR, highlightthickness=1,
    borderwidth=1, relief='solid'
)
prompt_textbox.grid(row=2, column=0, columnspan=2, sticky='NSEW', padx=5, pady=5)
prompt_textbox.configure(font=('Segoe UI', 12))
prompt_frame.rowconfigure(2, weight=1)

# Include transcript checkbox
include_transcript_var = tk.BooleanVar(value=False)
include_transcript_check = ttk.Checkbutton(
    prompt_frame, text="Include transcript", variable=include_transcript_var
)
include_transcript_check.grid(row=3, column=0, sticky='W', padx=5, pady=5)

# Copy prompt button
copy_prompt_button = ttk.Button(prompt_frame, text="Copy Prompt", command=copy_prompt)
copy_prompt_button.grid(row=3, column=1, pady=5, sticky='E')

# Set the focus to the URL entry field when the application starts
url_entry.focus()

# Run the GUI event loop
root.mainloop()
