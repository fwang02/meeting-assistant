import os
import pprint

from fastapi import FastAPI, UploadFile, File, HTTPException
from services import transcribe_audio, generate_summary, extract_tasks

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/meeting-summary/")
async def create_meeting_summary(file: UploadFile = File(...)):
    """
    Endpoint to upload an audio file and get a summary of the meeting.
    """
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.mp4')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .mp3, .wav, and .m4a files are supported.")

    # Save the uploaded file temporarily
    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    try:
        # Transcribe the audio file
        transcription = transcribe_audio(temp_file_path)
        # Generate a summary of the transcription
        summary = generate_summary(transcription)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    return {"transcript": transcription, "summary": summary}


@app.post("/meeting-tasks/")
async def create_meeting_tasks(file: UploadFile = File(...)):
    """
    Endpoint to upload an audio file and get tasks from the meeting.
    """
    if not file.filename.endswith(('.mp3', '.wav', '.m4a', '.mp4')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .mp3, .wav, and .m4a files are supported.")

    # Save the uploaded file temporarily
    temp_file_path = f"/tmp/{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    try:
        # Transcribe the audio file
        transcription = transcribe_audio(temp_file_path)
        # Generate a summary of the transcription
        tasks = extract_tasks(transcription)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    return {"transcript": transcription, "tasks": tasks}
