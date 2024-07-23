from transformers import AutoProcessor, AutoModelForVision2Seq


def process_images_to_texts(images_by_slide, text_content_by_slide):
    model = AutoModelForVision2Seq.from_pretrained("microsoft/kosmos-2-patch14-224")
    processor = AutoProcessor.from_pretrained("microsoft/kosmos-2-patch14-224")
    

    all_images_texts = []
    
    for slide_number, images in images_by_slide.items():
        slide_texts = set()

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

            if "background" not in caption:
                slide_texts.add(caption)

        if slide_texts:
            formatted_texts = "\n\n".join(slide_texts)
            all_images_texts.append(f"{formatted_texts}")
        else:
            all_images_texts.append("")

    return all_images_texts, text_content_by_slide

