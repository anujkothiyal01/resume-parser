import streamlit as st
import fitz  # PyMuPDF
import re

parsed_content = {}
def extract_text(uploaded_file):
    text = ""
    pdf_document = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

st.title('Resume Parser')
st.write('Upload Your Resume')

uploaded_file = st.file_uploader('Choose a file')

if uploaded_file is not None:
    with st.spinner('Processing....'):
        extracted_text = extract_text(uploaded_file)

    def get_email(extracted_text):
        r = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        return r.findall(extracted_text)

    email = get_email(extracted_text)
    parsed_content['Email'] = email

    # --------------------------------------------------------------------------------
    def get_phone(string):
        r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        phone_numbers = r.findall(string)
        return [re.sub(r'\D', '', num) for num in phone_numbers]


    phone_number = get_phone(extracted_text)
    if len(phone_number) <= 10:
        parsed_content['Phone'] = phone_number
    # ----------------------------------------------------------------------------------

    import spacy

    nlp = spacy.load('en_core_web_sm')
    from spacy.matcher import Matcher

    matcher = Matcher(nlp.vocab)


    def extract_name(text):
        nlp_text = nlp(text)

        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

        matcher.add('NAME', [pattern], on_match=None)

        matches = matcher(nlp_text)

        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    name = extract_name(extracted_text)
    print(name)
    parsed_content['Name'] = name

    st.subheader(parsed_content['Name'])
    st.text(parsed_content['Email'][0])
    st.text(parsed_content['Phone'][0])
