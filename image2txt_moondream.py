from transformers import AutoTokenizer, AutoModelForCausalLM
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image
import io


# 추출한 이미지를 텍스트로 변환하는 함수
def process_images_to_texts(images_by_slide, text_content_by_slide):
    model_id = "vikhyatk/moondream2"
    revision = "2024-08-26"
    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, revision=revision
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

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
                    slide_texts.add(response.strip())
            except Exception as e:
                print(f"Error processing image on {slide_number}: {e}")

        if slide_texts:
            formatted_texts = "\n\n".join(slide_texts)
            slide_index = int(slide_number.split()[-1]) - 1
            all_images_texts[slide_index] = formatted_texts

    return all_images_texts, text_content_by_slide

