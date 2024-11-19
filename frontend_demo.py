import streamlit as st
import requests
import time

st.title("PPT Script Generator")

uploaded_file = st.file_uploader("Upload your PPT file", type=["ppt", "pptx"])

url = "http://127.0.0.1:8000/"

if uploaded_file:
    with st.spinner("Uploading file..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.ms-powerpoint")}
        response = requests.post(url+"upload/", files=files)
        if response.status_code == 200:
            task_id = response.json()["task_id"]
            st.success(f"File uploaded! Task ID: {task_id}")
        else:
            st.error("Failed to upload file.")
            st.stop()

    requests.post(url + f"start_processing/{task_id}")

    # 상태 확인 및 대본 생성 확인
    status_url = url+f"status/{task_id}"
    script_url = url+f"script/{task_id}"

    status = "uploaded"
    while status != "completed":
        time.sleep(1)
        print("요청 보냄")
        status_response = requests.get(status_url)
        if status_response.status_code == 200:
            status_data = status_response.json()
            status = status_data["status"]
            st.write(f"Current status: {status}")
        else:
            st.error("Failed to fetch status.")
            st.stop()

    if status == "completed":
        st.success("Script generation completed!")
        script_response = requests.get(script_url)
        if script_response.status_code == 200:
            st.text_area("Generated Script:", script_response.text, height=400)
        else:
            st.error(script_response.json().get("error", "Unknown error"))
