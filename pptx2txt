import os
from pptx import Presentation

def extract_text(ppt_file):
    presentation = Presentation(ppt_file)
    text_content = []
    for slide_number, slide in enumerate(presentation.slides, start=1):
        slide_text = [f'--- Slide {slide_number} ---']
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_text = paragraph.text.strip()
                    if paragraph_text:
                        slide_text.append(paragraph_text)
        if len(slide_text) > 1:
            text_content.append('\n'.join(slide_text))
    return '\n\n'.join(text_content)

def save_text_to_file(text, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def process_ppt(ppt_file_path):
    # 파일 이름과 디렉토리 추출
    base_name = os.path.splitext(os.path.basename(ppt_file_path))[0]
    result_dir_path = os.path.join(os.path.dirname(ppt_file_path), 'result')
    result_file_path = os.path.join(result_dir_path, base_name + '.txt')

    # 텍스트 추출 및 저장
    extracted_text = extract_text(ppt_file_path)
    save_text_to_file(extracted_text, result_file_path)

    print(f'Text extracted and saved to {result_file_path}')

# 실제 사용 예시는 이 부분을 제거하고 프론트엔드에서 전달받은 경로를 사용. (사용해보고 싶다면 각주 풀고 사용)
# process_ppt('/path/to/presentation.pptx')
