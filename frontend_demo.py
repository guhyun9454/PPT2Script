import streamlit as st
import requests

st.title("PPT Script Generator")
st.write("Upload your PPT file, and the script will be generated automatically.")

# 파일 업로드
uploaded_file = st.file_uploader("Choose a PPT file", type=["ppt", "pptx"])

if uploaded_file:
    # FastAPI로 파일 전송
    with st.spinner("Uploading and processing..."):
        files = {"file": (uploaded_file.name, uploaded_file, "application/vnd.ms-powerpoint")}
        response = requests.post("http://127.0.0.1:8000/upload/", files=files)
    
    # 결과 출력
    if response.status_code == 200:
        data = response.json()
        if "content" in data:
            st.success("File processed successfully!")
            st.write("Extracted Script:")
            st.text(data["content"])
        else:
            st.error("Error: " + data.get("error", "Unknown error"))
    else:
        st.error("Failed to process the file. Please try again.")
