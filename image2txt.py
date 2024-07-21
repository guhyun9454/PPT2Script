import os
from PIL import Image
from transformers import AutoProcessor, AutoModelForVision2Seq

# 모델과 프로세서 로드
model = AutoModelForVision2Seq.from_pretrained("microsoft/kosmos-2-patch14-224")
processor = AutoProcessor.from_pretrained("microsoft/kosmos-2-patch14-224")

# 로컬 이미지 파일 경로 설정
image_path = "new_image.jpg"  # 여기에 실제 이미지 경로 입력

# 이미지 로드
image = Image.open(image_path)

# 입력 준비
inputs = processor(text="<grounding>An image of", images=image, return_tensors="pt")

# 텍스트 생성
generated_ids = model.generate(
    pixel_values=inputs["pixel_values"],
    input_ids=inputs["input_ids"],
    attention_mask=inputs["attention_mask"],
    image_embeds_position_mask=inputs["image_embeds_position_mask"],
    use_cache=True,
    max_new_tokens=128,
)
generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

# 결과 처리
processed_text, _ = processor.post_process_generation(generated_text)

# 결과 저장 디렉토리 및 파일 이름 설정
result_dir = "./result_image"
os.makedirs(result_dir, exist_ok=True)  # 디렉토리가 없으면 생성
image_filename = os.path.basename(image_path)  # 이미지 파일 이름 추출
text_filename = os.path.splitext(image_filename)[0] + '.txt'  # 확장자를 .txt로 변경

# 텍스트 파일로 결과 저장
result_path = os.path.join(result_dir, text_filename)
with open(result_path, 'w', encoding='utf-8') as f:
    f.write(processed_text)

print(f"Generated text saved to {result_path}")
