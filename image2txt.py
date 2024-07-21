
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
import os
from pptx2txt import extract_text_and_images
import re

def process_images_to_texts(images_by_slide, output_dir, ppt_file_path):
    model = AutoModelForVision2Seq.from_pretrained("microsoft/kosmos-2-patch14-224")
    processor = AutoProcessor.from_pretrained("microsoft/kosmos-2-patch14-224")
    base_name = os.path.splitext(os.path.basename(ppt_file_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    final_text_file_path = os.path.join(output_dir, f'all_{base_name}.txt')

    all_texts = []

    for slide, images in images_by_slide.items():
        slide_texts = set()  # 중복을 방지하기 위해 set 사용

        for index, image in enumerate(images):
            prompt = "<grounding> An image of"
            inputs = processor(text=prompt, images=image, return_tensors="pt")
            generated_ids = model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                image_embeds=None,
                image_embeds_position_mask=inputs["image_embeds_position_mask"],
                use_cache=True,
                max_new_tokens=64,
            )
            generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            caption, entities = processor.post_process_generation(generated_text)

            # "background"가 포함된 문구 제외
            if "background" not in caption:
                slide_texts.add(caption)  # 중복 제거를 위해 set에 추가

        if slide_texts:
            formatted_texts = "\n\n".join(slide_texts)  # Set에서 중복 제거된 텍스트를 조합
            all_texts.append(f"--- {slide} ---\n" + formatted_texts)
    
    with open(final_text_file_path, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(all_texts))

    print(f"Generated text saved in file: {final_text_file_path}")

# 이미지 추출 및 텍스트 처리 예시
images_by_slide = extract_text_and_images('./test.pptx')
ppt_file_path = "./test.pptx"
process_images_to_texts(images_by_slide, './result_image2txt', ppt_file_path)
