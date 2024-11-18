import os
from pptx_conversion import extract_text_and_images
from image2txt_moondream import process_images_to_texts
from pptx_charts_tables_extractor import extract_tables, extract_charts

def merge_text_and_images(ppt_file_path, output_dir):
    images_by_slide, text_content_by_slide = extract_text_and_images(ppt_file_path)
    all_images_text, text_content_by_slide = process_images_to_texts(images_by_slide, text_content_by_slide)
    tables_data = extract_tables(ppt_file_path)
    charts_data = extract_charts(ppt_file_path)

   
    print("Tables data length:", tables_data)
    print("Charts data length:", len(charts_data))


    # 결과 저장 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(ppt_file_path))[0]
    final_text_file_path = os.path.join(output_dir, f'all_{base_name}.txt')

    with open(final_text_file_path, 'w', encoding='utf-8') as file:
        for slide_number, (text_content, slide_texts, slide_tables, slide_charts) in enumerate(zip(text_content_by_slide, all_images_text, tables_data, charts_data), start=1):
            print(f"Processing slide {slide_number}")
            
            slide_header = f"--- Slide {slide_number} ---"
            print(f"Writing slide header: {slide_header}")
            file.write(slide_header + "\n")

            # 이미지 텍스트 먼저 추가
            if slide_texts:
                print(f"Writing slide texts: {slide_texts.strip()}")
                file.write("\n\n" + slide_texts.strip() + "\n\n")  # 불필요한 공백 제거
            
            # 슬라이드 텍스트 추가
            if text_content:
                print(f"Writing slide content: {text_content.strip()}")
                file.write("\n\n" + text_content.strip() + "\n\n")  # 불필요한 공백 제거
            
            # 표 데이터 추가
            if slide_tables:
                combined_tables = "\n\n".join(slide_tables)
                print(f"Writing tables: {combined_tables.strip()}")
                file.write("\n\n" + combined_tables.strip() + "\n\n")  # 불필요한 공백 제거

            # 차트 데이터 추가
            if slide_charts:
                combined_charts = "\n\n".join(slide_charts)
                print(f"Writing charts: {combined_charts.strip()}")
                file.write("\n\n" + combined_charts.strip() + "\n\n")  # 불필요한 공백 제거

            file.write("\n\n")
            print("Finished writing slide\n")

    print(f"Generated text saved in file: {final_text_file_path}")

# 예시 (사용시 각주 제거 후 사용)
if __name__ == "__main__":
    ppt_file_path = "./test.pptx"
    output_dir = './result_txt'
    merge_text_and_images(ppt_file_path, output_dir)
