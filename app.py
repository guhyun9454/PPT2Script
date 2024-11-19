from merge_txt import ppt2txt

from fastapi import FastAPI, File, UploadFile
import shutil
from pathlib import Path

app = FastAPI()

@app.post("/upload/")
async def upload_ppt(file: UploadFile = File(...)):
    # 파일 저장 경로 설정
    file_location = f"uploaded_files/{file.filename}"
    Path("uploaded_files").mkdir(parents=True, exist_ok=True)
    
    # 파일 저장
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # ppt2txt 함수 호출
    try:
        extracted_text = ppt2txt(ppt_file_path=file_location)
        return {"filename": file.filename, "content": extracted_text}
    except Exception as e:
        return {"error": str(e)}