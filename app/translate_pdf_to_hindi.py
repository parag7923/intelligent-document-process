import PyPDF2
import docx
from googletrans import Translator

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text.strip()

def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text.strip()

def translate_pdf_to_hindi(file, file_type):
    if file_type == 'pdf':
        text = extract_text_from_pdf(file)
    elif file_type == 'docx':
        text = extract_text_from_docx(file)
    
    if not text.strip():
        return "Error: The document contains no readable text."

    translator = Translator()
    chunk_size = 5000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_text = ""

    for chunk in chunks:
        translated_chunk = translator.translate(chunk, src='en', dest='hi').text
        translated_text += translated_chunk + "\n\n"

    return translated_text.strip()
