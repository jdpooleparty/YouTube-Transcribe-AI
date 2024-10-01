#Initial Setup
1. create venv: 
    a. python -m venv venv312
2. activate venv:
    a. venv312\Scripts\activate 
3. Upgrate pip
    a. python.exe -m pip install --upgrade pip
4. run requirements.txt
    a. pip install -r requirements.txt
5. set env variables
    a. setx OPENAI_API_KEY "your-api-key-here"
    b. setx OPENAI_ORGANIZATION "your-organization-id-here"


#To set up an executable:
1. pip install pyinstaller
2. pyinstaller --onefile --windowed youtube_transcript_getter.py
3. grab exe from source directory