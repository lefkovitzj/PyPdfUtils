"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 2/28/2024
    Project Name: PyPdfUtils
    File Name: operations/compression.py
"""

import fitz
import datetime
import os

def calculate_pdf_temp_title(action):
    tb = str(datetime.datetime.today()) # Basic timestamp string, with the type of action included.
    file_title = tb[:4] + "-" + tb[5:7] + "-" + tb[8:10] + "_" + tb[11:13] + "-" + tb[14:16] + "-" + tb[17:19] + "_" + action + ".pdf"
    return file_title

class PDF_Compressor():
    def __init__(self, fitz_doc):
        """ Initialize the object. """
        if "temporary_files" not in os.listdir(os.getcwd()): # Ensure that the necessary save folder exists.
            os.makedirs("temporary_files") 
        self.doc = fitz_doc
    def compress_basic(self):
        self.doc.save("temporary_files\\" + calculate_pdf_temp_title("compress"), deflate=True) # Save a copy of the document, but compress the document.
        return True, "temporary_files\\" + calculate_pdf_temp_title("compress")
    def compress_max(self):
        self.doc.save("temporary_files\\" + calculate_pdf_temp_title("compress_max"), deflate=True, garbage=4, deflate_images=True, deflate_fonts=True) # Save a copy of the document, but compress and collect garbage.
        return True, "temporary_files\\" + calculate_pdf_temp_title("compress_max")
