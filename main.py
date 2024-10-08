import streamlit as st
import os
from app.pdf_summary_generator import pdf_summary_generator
from app.translate_pdf_to_hindi import translate_pdf_to_hindi

# Set the page configuration
st.set_page_config(page_title="Intelligent Document Processing", layout="wide")

# Add a title and a subtitle
st.title("📄 Intelligent Document Processing")
st.subheader("Transform your documents effortlessly!")

# Sidebar for file uploader
st.sidebar.header("Upload Your Document")
uploaded_file = st.sidebar.file_uploader("Choose a PDF or DOCX file:", type=["pdf", "docx"])

if uploaded_file:
    st.success("File uploaded successfully!")  
    file_type = uploaded_file.name.split('.')[-1].lower()  # Determine file type

    # Processing options
    option = st.selectbox("Choose a processing option:", 
                          ("PDF Summary Generator", 
                           "Language Conversion (English to Hindi)"))

    if st.button("Process"):
        with st.spinner("Processing..."):
            if option == "PDF Summary Generator":
                summary = pdf_summary_generator(uploaded_file, file_type)
                st.subheader("📝 Summary")
                st.write(summary)

            elif option == "Language Conversion (English to Hindi)":
                translated_text = translate_pdf_to_hindi(uploaded_file, file_type)
                st.subheader("🌐 Translated Text")
                st.write(translated_text)


