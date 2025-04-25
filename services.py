import json
import os
import whisper
from openai import OpenAI
from dotenv import load_dotenv

from utils import remove_first_and_last_line

load_dotenv()
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")


def transcribe_audio(audio_path) -> str:
    """
    Transcribe an audio file using OpenAI's Whisper model.
    """
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]


def generate_summary(text: str) -> str:
    """
    Generate a summary of the provided text using DeepSeek Chat model.
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个会议助手，擅长将会议记录进行摘要。"},
            {"role": "user", "content": f"请对以下会议内容进行总结：\n{text}"}
        ]
    )
    return response.choices[0].message.content.strip()


def extract_tasks(text: str) -> list:
    """
    Extract tasks from the provided text using DeepSeek Chat model.
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个会议助手，擅长从会议记录中提取任务。"},
            {"role": "user", "content": f"请从以下会议内容中提取任务，使用json格式：\n{text}"}
        ]
    )
    response_content = remove_first_and_last_line(response.choices[0].message.content)
    parsed_content = json.loads(response_content)
    tasks = parsed_content.get("tasks", [])

    return tasks
