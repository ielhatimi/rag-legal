import json

import numpy as np
import pymupdf

from config import CONTEXT_SIZE, WINDOW_SIZE


def open_pdf(file_path):
    """
    Opens a PDF file and returns the document object.

    :param file_path: Path to the PDF file.
    :return: Document object of the opened PDF.
    """
    try:
        doc = pymupdf.open(file_path)
        return doc
    except Exception as e:
        print(f"Error opening PDF file: {e}")
        return None


def extract_text_from_pdf(doc):
    """
    Extracts chunks of WINDOW_SIZE words from each page of the PDF document, with a context of CONTEXT_SIZE words.

    :param doc: Document object of the opened PDF.
    :return: List of strings, each containing WINDOW_SIZE words from the document.
    """
    if not doc:
        return []

    extracted_chunks = []
    chunks_list = []
    for page in doc:
        page_text = page.get_text()
        page_text_list = page_text.split()
        if len(page_text_list) < WINDOW_SIZE:
            print(f"Document is short. Size is : {len(page_text_list)}")
            chunks_list.append(" ".join(page_text_list))
            continue
        for i in range(
            0,
            len(page_text_list) - WINDOW_SIZE + 1,
            WINDOW_SIZE - CONTEXT_SIZE,
        ):
            print(f"Document size is : {len(page_text_list)}")
            chunks_list.append(" ".join(page_text_list[i : i + WINDOW_SIZE]))
        size_last_chunk = len(page_text_list) % WINDOW_SIZE
        if size_last_chunk != 0:
            # Adding the last chunk if not already added
            last_chunk = " ".join(
                page_text_list[-(size_last_chunk + CONTEXT_SIZE) :]
            )
            chunks_list.append(last_chunk)
    print(f"len(chunks_list): {len(chunks_list)}")
    for i, chunk in enumerate(chunks_list):
        extracted_chunks.append({"id_chunk": i, "chunk": chunk})
    return extracted_chunks


def save_chunks(extracted_chunks):
    """
    Saves the extracted chunks to a JSON file.

    :param extracted_chunks: List of extracted chunks.
    """
    with open("./data/processed/extracted_chunks.json", "w") as f:
        json.dump(extracted_chunks, f, indent=2)
