from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
import torch

def process_images_to_texts(images_by_slide, text_content_by_slide):
    # 모델 및 토크나이저 로드
    model_id = "vikhyatk/moondream2"
    revision = "2024-03-06"
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True, revision=revision,device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    # 슬라이드 키를 정수로 변환
    try:
        slide_mapping = {int(key.split()[-1]): value for key, value in images_by_slide.items()}
    except ValueError:
        raise ValueError("Slide keys in images_by_slide must end with an integer (e.g., 'Slide 1').")

    # 슬라이드 수 계산
    num_slides = max(slide_mapping.keys()) if slide_mapping else 0
    all_images_texts = [''] * num_slides

    for slide_number, images in slide_mapping.items():
        slide_texts = set()  # 중복 제거를 위한 집합

        if not images:  # 이미지가 없는 경우 스킵
            continue

        for image in images:
            try:
                # Convert PIL image to tensor
                image_tensor = torch.tensor(image).to("cuda")  # Move image tensor to GPU
                enc_image = model.encode_image(image_tensor)
                query = "Describe this image."
                response = model.answer_question(enc_image, query, tokenizer)

                if response:
                    slide_texts.add(response.strip())  # Add after stripping whitespace
            except Exception as e:
                print(f"Error processing image on slide {slide_number}: {e}")
                continue

        # 슬라이드 텍스트 포맷팅 및 저장
        if slide_texts:
            formatted_texts = "\n\n".join(slide_texts)
            all_images_texts[slide_number - 1] = formatted_texts  # 슬라이드 번호에 맞게 저장

    return all_images_texts, text_content_by_slide
