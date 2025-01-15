# Developer: Eric Neftali Paiz
import os
import fitz

UPLOAD_DIR = "data/uploaded"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path

def extract_text_from_pdf(filename: str):
    try:
        doc = fitz.open(filename=filename)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")
    
def prompt_save_text(text: str):
    save_name = input("Enter the filename to save the extracted text (e.g., output.txt): ").strip()
    if not save_name.endswith(".txt"):
        save_name += ".txt"
    save_path = os.path.join(UPLOAD_DIR, save_name)

    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text Successfully saved as {save_path}")
    except Exception as e:
        print(f"Failed to save text file: {e}")

    