from transformers import AutoTokenizer, AutoModelForCausalLM
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image
import io


# 텍스트 필터링 함수
def filter_descriptions(description):
    # 불필요한 텍스트를 필터링하기 위한 키워드 목록
    exclusion_keywords = [
        "solid color",
        "devoid of",
        "no discernible",
        "monochromatic",
        "minimalist aesthetic",
        "empty",
        "unbroken",
    ]
    
    # 키워드가 포함된 경우 빈 문자열 반환
    for keyword in exclusion_keywords:
        if keyword in description.lower():
            return ""
    
    return description


# 추출한 이미지를 텍스트로 변환하는 함수
def process_images_to_texts(model, tokenizer, images_by_slide, text_content_by_slide):



    # 텍스트 데이터를 슬라이드 수만큼 초기화
    all_images_texts = [''] * len(text_content_by_slide)

    for slide_number, images in images_by_slide.items():
        slide_texts = set()

        for index, image in enumerate(images):
            try:
                # 모델로 이미지 인코딩
                enc_image = model.encode_image(image)

                # 질문 생성 및 응답
                query = "Describe this image."
                response = model.answer_question(enc_image, query, tokenizer)

                if response:
                    # 응답을 필터링
                    filtered_response = filter_descriptions(response.strip())
                    if filtered_response:  # 필터링 후 내용이 있으면 추가
                        slide_texts.add(filtered_response)
            except Exception as e:
                print(f"Error processing image on {slide_number}: {e}")

        if slide_texts:
            formatted_texts = "\n\n".join(slide_texts)
            slide_index = int(slide_number.split()[-1]) - 1
            all_images_texts[slide_index] = formatted_texts

    return all_images_texts, text_content_by_slide
