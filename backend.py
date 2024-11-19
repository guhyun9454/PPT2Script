from fastapi import FastAPI, File, UploadFile
from pathlib import Path
import asyncio
import uuid
from openai import OpenAI  
from typing import Dict
from dotenv import load_dotenv
import os
from merge_txt import ppt2txt


load_dotenv()

api_key = os.getenv("OPENAI_API")

def make_prompt(text):
    return f"""You are an assistant that generates scripts for presentations. Given the content from a PowerPoint slide deck, create a script for the presenter to use. 

    The content of the slides is as follows:

    {text}

    Please write a detailed, engaging script tailored to the given slides.
    answer in korean"""

app = FastAPI()

# 작업 상태 저장: uploaded, processing_ai, generating_script, completed, error
tasks: Dict[str, Dict] = {}

client = OpenAI(api_key=api_key)

@app.post("/upload/")
async def upload_ppt(file: UploadFile = File(...)):
    # 작업 ID 생성
    task_id = str(uuid.uuid4())
    file_path = f"uploaded_files/{task_id}_{file.filename}"
    Path("uploaded_files").mkdir(parents=True, exist_ok=True)

    # 파일 저장
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 상태 초기화
    tasks[task_id] = {"status": "uploaded", "result": None, "file_path": file_path}

    return {"task_id": task_id}

@app.post("/start_processing/{task_id}")
async def start_processing(task_id: str):
    # 작업 ID 확인
    print("start processing: ",task_id)

    if task_id not in tasks:
        return {"error": "Task not found"}

    # 이미 처리 중인 작업인지 확인
    if tasks[task_id]["status"] not in ["uploaded"]:
        return {"error": "Task is already being processed or completed"}

    # 작업 비동기 처리 시작
    file_path = tasks[task_id]["file_path"]
    print(f"{task_id} 처리에 진입합니다.")
    asyncio.create_task(process_ppt(file_path, task_id))

    print(f"---")

    tasks[task_id]["status"] = "processing_ai"
    return {"message": f"Processing started for task_id: {task_id}"}

# 진행 상태 조회
@app.get("/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found"}
    return tasks[task_id]


@app.get("/script/{task_id}")
async def get_script(task_id: str):
    if task_id not in tasks:
        return {"error": "Task not found"}

    if tasks[task_id]["status"] != "completed":
        return {"error": "Task not completed yet"}

    result = tasks[task_id]["result"]
    return {"script": result}

    
async def process_ppt(file_path: str, task_id: str):
    try:
        print(f"Task {task_id}: Started processing")

        # PPT -> 텍스트 변환 (CPU 바운드 작업을 비동기로 실행)
        tasks[task_id]["status"] = "processing_ai"
        text = await asyncio.to_thread(ppt2txt, file_path)

        print("텍스트 변환 성공. 대본 생성 시작")

        # 텍스트 -> 대본 생성 (I/O 바운드 작업 처리)
        tasks[task_id]["status"] = "generating_script"
        prompt = make_prompt(text)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
        )

        tasks[task_id]["result"] = response.choices[0].message.content
        tasks[task_id]["status"] = "completed"
        print(f"Task {task_id}: Processing completed")
    except Exception as e:
        tasks[task_id]["status"] = "error"
        tasks[task_id]["result"] = str(e)
        print(f"Task {task_id}: Error occurred - {str(e)}")

