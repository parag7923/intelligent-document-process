import PyPDF2
import docx
from transformers import pipeline

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:  # Only add non-empty text
            text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(docx_file):
    """Extract text from a DOCX file."""
    doc = docx.Document(docx_file)
    text = '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])  # Skip empty paragraphs
    return text.strip()

def pdf_summary_generator(file, file_type, max_length=150, min_length=50):
    """Generate a summary for the given document."""
    if file_type == 'pdf':
        text = extract_text_from_pdf(file)
    elif file_type == 'docx':
        text = extract_text_from_docx(file)
    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."

    if len(text) == 0:
        return "No text found in the document to summarize."

    # Split text into manageable chunks for summarization
    max_chunk_size = 1024  
    chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

    # Initialize the summarizer
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn")

    summary = ''
    try:
        for chunk in chunks:
            # Summarize each chunk
            summary_chunk = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summary += f"\n{summary_chunk[0]['summary_text']}\n\n"  # Add formatting for clarity
        return summary.strip() or "Summary generated is empty."
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

# Optional: Add a function to enhance summaries with headings
def enhance_summary_with_headings(summary):
    """Enhance the summary by adding headings for each section."""
    sections = summary.split("\n\n")
    enhanced_summary = ""
    for i, section in enumerate(sections, start=1):
        enhanced_summary += f"### Section {i}\n{section}\n\n"  # Use markdown headings for sections
    return enhanced_summary.strip()
