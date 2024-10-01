# Initial Setup
1. Clone Repo
2. Create Virtual Environment: python -m venv venv312
3. Activate venv: venv312\Scripts\activate 
4. Upgrade pip: python.exe -m pip install --upgrade pip
5. Install requirements.txt: pip install -r requirements.txt
6. Run main program: python -m youtube_transcribe_ai


# To set Up Main Program as an Executable:
1. Pip install pyinstaller
2. Pyinstaller --onefile --windowed youtube_transcribe_ai.py
3. Grab exe from source directory and place where it will be handy


# Bonus
_summarize_transcript_gpt.py_ can be retrofitted to automate GPT summaries using Open API. Let me know if there is interest in a similar program that automates GPT integration.