import streamlit as st
import openai
import yaml
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

# Open Credentials

try:
    with open('chatgpt_api_credentials1.yml', 'r') as file:
        creds = yaml.safe_load(file)
except:
    creds = {}

# Open Sidebar
with st.sidebar:
    openai_api_key = creds.get('openai_key', '')

    if openai_api_key:
        st.text("OpenAI API Key provided")
    else:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    # adding a hyperlink
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# Set Title:
st.title("📝 File Q&A with ChatGPT")

# Upload the file:
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md", "pdf"))

# Text input:
question = st.text_input(
    "Ask something about the article",
    placeholder="Can you give me a short summary?",
    disabled=not uploaded_file
)
if uploaded_file and question and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

if uploaded_file and question and openai_api_key:
    # Parsing the text:

    if uploaded_file.type == "application/pdf":
      #do later
      output_string = StringIO()
      parser = PDFParser(uploaded_file)
      doc = PDFDocument(parser)
      rsrcmgr = PDFResourceManager()
      device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
      interpreter = PDFPageInterpreter(rsrcmgr, device)
      for page in PDFPage.create_pages(doc):
          interpreter.process_page(page)

      article = output_string.getvalue()

    else:
      article = uploaded_file.read().decode()

    # Prompting:
    my_prompt = f"""Here's an article {article}.\n\n
        \n\n\n\n{question}"""

    # ChatGPT Connection:
    openai.api_key = openai_api_key

    messages = [{"role": "user", "content": my_prompt}]
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )

    #response

    st.write("### Answer")
    st.write(response.choices[0].message.content)