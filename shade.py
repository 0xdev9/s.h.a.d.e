import os
import fitz  # PyMuPDF
from PIL import Image

def clean_pdf_metadata(input_path, output_path):
    try:
        doc = fitz.open(input_path)
        new_doc = fitz.open()
        for page in doc:
            new_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)
        new_doc.set_metadata({})
        new_doc.save(output_path)
        new_doc.close()
        return True, f"Metadata removed for: {input_path}"
    except Exception as e:
        return False, f"Error processing PDF: {e}"

def clean_image_metadata(input_path, output_path):
    try:
        image = Image.open(input_path)
        data = list(image.getdata())
        image_no_exif = Image.new(image.mode, image.size)
        image_no_exif.putdata(data)
        image_no_exif.save(output_path)
        return True, f"Metadata removed for: {input_path}"
    except Exception as e:
        return False, f"Error processing image: {e}"

def process_file(input_path, output_folder):
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}_anonymized{ext}")
    if ext.lower() == '.pdf':
        return clean_pdf_metadata(input_path, output_path)
    elif ext.lower() in ['.jpg', '.jpeg', '.png']:
        return clean_image_metadata(input_path, output_path)
    else:
        return False, f"Unsupported format: {filename}"

def main():
    input_path = input("Enter the path to the input file: ")
    output_folder = input("Enter the path to the output folder: ")
    if not os.path.exists(input_path):
        print("Input file does not exist.")
        return
    if not os.path.isdir(output_folder):
        print("Output folder does not exist.")
        return
    success, message = process_file(input_path, output_folder)
    print(message)

if __name__ == "__main__":
    main()
