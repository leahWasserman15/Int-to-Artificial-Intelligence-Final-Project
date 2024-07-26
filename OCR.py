import os
import torch
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from PIL import Image
import io

# Set environment variable
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Model and device setup
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model_id = "google/paligemma-3b-mix-224"

# Load model and processor
model = PaliGemmaForConditionalGeneration.from_pretrained(model_id).to(device)
processor = AutoProcessor.from_pretrained(model_id)

def extract_text_from_image(image_content):
    image = Image.open(io.BytesIO(image_content))

    # Prompt for detecting text
    prompt = "Extract all relevant details from this invoice."

    # Prepare inputs for the model
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device)
    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        # Generate the output
        generation = model.generate(**inputs, max_new_tokens=100, do_sample=False)
        generation = generation[0][input_len:]
        decoded = processor.decode(generation, skip_special_tokens=True)

    return decoded

def extract_text_from_pdf(pdf_content):
    # For simplicity, let's assume you're converting the PDF to images first
    # You may use libraries like pdf2image to convert PDF pages to images
    # Then call extract_text_from_image for each image
    pass

def extract_invoice_details(text):
    # Implement your logic to extract invoice details from the text
    details = {}
    # Example extraction logic
    details['Invoice Number'] = re.search(r'Invoice Number: (\S+)', text).group(1) if re.search(r'Invoice Number: (\S+)', text) else 'N/A'
    details['Amount'] = re.search(r'Total Amount Due: (\S+)', text).group(1) if re.search(r'Total Amount Due: (\S+)', text) else 'N/A'
    details['Invoice Date'] = re.search(r'Invoice Date: (\S+)', text).group(1) if re.search(r'Invoice Date: (\S+)', text) else 'N/A'
    details['Due Date'] = re.search(r'Due Date: (\S+)', text).group(1) if re.search(r'Due Date: (\S+)', text) else 'N/A'
    return details
