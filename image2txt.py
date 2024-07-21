from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq
import os

def process_images_to_texts(images_by_slide, output_dir, ppt_file_path):
    # 모델과 프로세서 로드
    model = AutoModelForVision2Seq.from_pretrained("microsoft/kosmos-2-patch14-224")
    processor = AutoProcessor.from_pretrained("microsoft/kosmos-2-patch14-224")
    base_name = os.path.splitext(os.path.basename(ppt_file_path))[0]
    os.makedirs(output_dir, exist_ok=True)
    final_text_file_path = os.path.join(output_dir, f'all_{base_name}.txt')


    all_texts = []

    # images_by_slide 딕셔너리 내의 각 슬라이드 이미지 리스트 순회
    for slide, images in images_by_slide.items():
       
        slide_texts = []

        # 각 이미지 처리
        for index, image in enumerate(images):
            # 이미지에서 텍스트 추출
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
            
            generated_text=processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            processed_text = processor.post_process_generation(generated_text, cleanup_and_extract=False)
            caption, entities = processor.post_process_generation(generated_text)
            slide_texts.append(caption)

        all_texts.append(f"--- {slide} ---\n" + "\n\n".join(slide_texts))
           
    with open(final_text_file_path, 'w', encoding='utf-8') as file:
        file.write("\n\n".join(all_texts))

    print(f"Generated text saved in directory: {output_dir}")

    

# 이미지 추출 및 텍스트 처리 예시
from pptx2txt import extract_text_and_images  # Adjust the import statement based on your actual file organization
# images_by_slide = extract_text_and_images('./test.pptx')
# ppt_file_path = "./test.pptx"
process_images_to_texts(images_by_slide, './result_image2txt', ppt_file_path)
