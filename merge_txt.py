import os
from pptx_conversion import extract_text_and_images
from image2txt import process_images_to_texts
from pptx_charts_tables_extractor import extract_tables, extract_charts

def merge_text_and_images(ppt_file_path, output_dir):
    images_by_slide, text_content_by_slide = extract_text_and_images(ppt_file_path)
    all_images_text, text_content_by_slide = process_images_to_texts(images_by_slide, text_content_by_slide)
    tables_data = extract_tables(ppt_file_path)
    charts_data = extract_charts(ppt_file_path)

    # 결과 저장 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(ppt_file_path))[0]
    final_text_file_path = os.path.join(output_dir, f'all_{base_name}.txt')

    # 최종 결과물 파일에 저장
    with open(final_text_file_path, 'w', encoding='utf-8') as file:
        for slide_number, (text_content, slide_texts, slide_tables, slide_charts) in enumerate(zip(text_content_by_slide, all_images_text, tables_data, charts_data),start=1):
            
            slide_header = f"--- Slide {slide_number} ---"
            file.write(slide_header + "\n")

            # 이미지 텍스트 먼저 추가
            if slide_texts:
                file.write("\n\n" + slide_texts.strip())  # 불필요한 공백 제거
            
            # 슬라이드 텍스트 추가
            if text_content:
                file.write("\n\n" + text_content.strip())  # 불필요한 공백 제거
            
            if slide_tables:
                combined_tables = "\n\n".join(slide_tables)
                file.write("\n\n" + combined_tables.strip() + "\n\n")

            if slide_charts:
                combined_charts = "\n\n".join(slide_charts)
                file.write("\n\n" + combined_charts.strip() + "\n\n") 

            file.write("\n\n")

    print(f"Generated text saved in file: {final_text_file_path}")



# 예시 (사용시 각주 제거 후 사용)
if __name__ == "__main__":
    ppt_file_path = "./test.pptx"
    output_dir = './result_txt'
    merge_text_and_images(ppt_file_path, output_dir)
