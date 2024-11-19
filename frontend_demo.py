import streamlit as st
import requests
import time

st.title("PPT2SCRIPT - TGTHON+")
st.caption("사진으로만 구성된 PPT는 사용할 수 없습니다.")
st.caption("의미없는 사진이 많을 시 잘 작동하지 않을 수 있습니다.")

uploaded_file = st.file_uploader("Upload your PPT file", type=["pptx"])

url = "http://127.0.0.1:8000/"

if uploaded_file:
    # 파일 업로드
    with st.spinner("업로드 대기중..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.ms-powerpoint")}
        response = requests.post(url + "upload/", files=files)
        if response.status_code == 200:
            task_id = response.json()["task_id"]
            st.success(f"File uploaded! Task ID: {task_id}")
        else:
            st.error("Failed to upload file.")
            st.stop()

    # 작업 실행
    with st.spinner("작업 대기중..."):
        start_response = requests.post(url + f"start_processing/{task_id}")
        if start_response.status_code != 200:
            st.error("Failed to start processing.")
            st.stop()

    # 상태 확인
    status_url = url + f"status/{task_id}"
    script_url = url + f"script/{task_id}"
    status_placeholder = st.empty()  # 상태 메시지를 동적으로 업데이트
    status = "uploaded"

    with st.spinner("AI 작업중..."):
        while status not in ["completed", "error"] :
            time.sleep(1)  # 1초 대기
            status_response = requests.get(status_url)
            if status_response.status_code == 200:
                status_data = status_response.json()
                status = status_data["status"]
            else:
                st.error("Failed to fetch status.")
                st.stop()

    # 작업 완료 후 결과 표시
    if status == "completed":
        script_response = requests.get(script_url)
        if script_response.status_code == 200:
            st.text_area("대본:", script_response.json()["script"], height=400)
        else:
            st.error("Failed to fetch script.")
    elif status == "error":
        # 오류 메시지 출력
        error_message = status_data.get("result", "An unknown error occurred.")
        st.error(f"Processing failed: {error_message}")