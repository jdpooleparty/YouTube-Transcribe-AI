# Initial Setup
1. Create Virtual Environment: python -m venv venv312
2. Activate venv: venv312\Scripts\activate 
3. Upgrade pip: python.exe -m pip install --upgrade pip
4. Install requirements.txt: pip install -r requirements.txt
5. Run main program: python -m youtube_transcribe_ai


# To set Up Main Program as an Executable:
1. Pip install pyinstaller
2. Pyinstaller --onefile --windowed youtube_transcribe_ai.py
3. Grab exe from source directory and place where it will be handy


# Bonus
_summarize_transcript_gpt.py_ can be retrofitted to automate GPT summaries using Open API. Let me know if there is interest in a similar program that automates GPT integration.