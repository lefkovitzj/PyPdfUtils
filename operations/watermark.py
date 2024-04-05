"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 4/4/2024
    Project Name: PyPdfUtils
    File Name: operations/watermark.py
"""

import fitz
import datetime
import os

def calculate_pdf_temp_title(action, file_ending=".pdf"):
    tb = str(datetime.datetime.today()) # Basic timestamp string, with the type of action included.
    file_title = tb[:4] + "-" + tb[5:7] + "-" + tb[8:10] + "_" + tb[11:13] + "-" + tb[14:16] + "-" + tb[17:19] + "_" + action + file_ending
    return file_title

class PDF_Watermarker():
    def __init__(self, fitz_doc):
        """ Initialize the object. """
        if "temporary_files" not in os.listdir(os.getcwd()): # Ensure that the necessary save folder exists.
            os.makedirs("temporary_files") 
        self.doc = fitz_doc
    def watermark(self, watermark_source_file):
        file_loc = "temporary_files\\" + calculate_pdf_temp_title("watermarked", ".pdf")
        for page in self.doc:
            if not page.is_wrapped: # Solution for flipped/rotated watermark without reason. Documentation: https://pymupdf.readthedocs.io/en/latest/recipes-common-issues-and-their-solutions.html#misplaced-item-insertions-on-pdf-pages
                page.wrap_contents()
            page.insert_image(page.bound(), filename = watermark_source_file, overlay = True)
        self.doc.save(file_loc)
        return True, file_loc