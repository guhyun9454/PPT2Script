from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image
import io
import os

def extract_text_and_images(ppt_file_path):
    presentation = Presentation(ppt_file_path)
    text_content_by_slide = []
    images_by_slide = {}

    for slide_number, slide in enumerate(presentation.slides, start=1):
        slide_text = []
        images = []

        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    paragraph_text = paragraph.text.strip()
                    if paragraph_text:
                        slide_text.append(paragraph_text)
            elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                # 이미지를 메모리에 저장
                image_stream = io.BytesIO(shape.image.blob)
                image = Image.open(image_stream)
                images.append(image)
        
        if images:
            images_by_slide[f"Slide {slide_number}"] = images
        
        if slide_text:
            text_content_by_slide.append('\n'.join(slide_text))


    
    return images_by_slide, text_content_by_slide


