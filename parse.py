import os
import shutil
import pdfplumber
import pandas as pd
import logging
import warnings

from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
warnings.filterwarnings("ignore")

CHROMA_PATH = "chroma"
DATA_PATH = "data"
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API")

logname = 'chromadb_log.log'  # Specify the log file name
logging.basicConfig(filename=logname,
                    filemode='w',  # Append to existing log, use 'w' to overwrite
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

def remove_header_footer(page, top_margin=90, bottom_margin=80):
    bottom_y = page.height
    page_text = page.crop((0, top_margin, page.width, bottom_y - bottom_margin)).extract_text()
    return page_text

def extract_content(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for idx, page in enumerate(pdf.pages):
            if idx == 0:
                text += remove_header_footer(page, top_margin=100, bottom_margin=100) + "\n"
            else:
                text += remove_header_footer(page) + "\n"
    return text[:text.find("\nReferences\n")]

def format_line(line):
    return line.replace("\n", " ").replace("„", "\"").replace("‟", "\"").strip()


def chunk_text(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )

    chunks = text_splitter.create_documents(text_splitter.split_text(text))
    return chunks

def save_to_chroma(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    try:
        embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        db = Chroma.from_documents(chunks, embedding_function, persist_directory=CHROMA_PATH)

        db.persist()
        print(f"Saved {len(chunks)} chunks to Chroma database.")
    except Exception as e:
        logging.exception("Failed to save chunks to Chroma DB")


