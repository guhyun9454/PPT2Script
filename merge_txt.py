from pptx_conversion import extract_text_and_images
from image2txt_moondream import process_images_to_texts
from pptx_charts_tables_extractor import extract_tables, extract_charts

def ppt2txt(ppt_file_path):
    # 슬라이드별 텍스트, 이미지 텍스트, 표 데이터, 차트 데이터 추출
    images_by_slide, text_content_by_slide = extract_text_and_images(ppt_file_path)
    all_images_text, text_content_by_slide = process_images_to_texts(images_by_slide, text_content_by_slide)
    tables_data = extract_tables(ppt_file_path)
    charts_data = extract_charts(ppt_file_path)

    # 결과를 저장할 문자열 초기화
    result_text = ""

    for slide_number, (text_content, slide_texts, slide_tables, slide_charts) in enumerate(
        zip(text_content_by_slide, all_images_text, tables_data, charts_data), start=1
    ):
        slide_header = f"--- Slide {slide_number} ---\n"
        result_text += slide_header

        # 이미지 텍스트 추가
        if slide_texts:
            result_text += f"\n\n{slide_texts.strip()}\n\n"

        # 슬라이드 텍스트 추가
        if text_content:
            result_text += f"\n\n{text_content.strip()}\n\n"

        # 표 데이터 추가
        if slide_tables:
            combined_tables = "\n\n".join(slide_tables)
            result_text += f"\n\n{combined_tables.strip()}\n\n"

        # 차트 데이터 추가
        if slide_charts:
            combined_charts = "\n\n".join(slide_charts)
            result_text += f"\n\n{combined_charts.strip()}\n\n"

    return result_text

# 예시 (사용시 각주 제거 후 사용)
if __name__ == "__main__":
    ppt_file_path = "./test.pptx"
    output = merge_text_and_images(ppt_file_path)
    print(output)  # 결과 문자열 출력
