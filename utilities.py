import os
import PyPDF2
from io import BytesIO

def extract_pdf_text(uploaded_file):
    """
    Extract text from uploaded PDF file
    """
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""

def save_uploaded_file(uploaded_file, directory='uploads'):
    """
    Save uploaded file to a specific directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path