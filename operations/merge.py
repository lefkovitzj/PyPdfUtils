"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 2/25/2024
    Project Name: PyPdfUtils
    File Name: operations/merge.py
"""

import fitz
import datetime
import os

def calculate_pdf_temp_title():
    tb = str(datetime.datetime.today()) # Basic timestamp string.
    file_title = tb[:4] + "-" + tb[5:7] + "-" + tb[8:10] + "_" + tb[11:13] + "-" + tb[14:16] + "-" + tb[17:19] + ".pdf"
    return file_title

class PDF_Merger():
    def __init__(self):
        """ Initialize the object. """
        if "temporary_files" not in os.listdir(os.getcwd()): # Ensure that the necessary save folder exists.
            os.makedirs("temporary_files") 
        self.included_pdf_objs = []
        self.preview_loc = calculate_pdf_temp_title()
        self.pages = []
        self.doc = fitz.open()
    def save(self):
        """ Save the document to temporary files. """
        self.doc.save("temporary_files\\" + self.preview_loc)
    def add_pages(self, source_file_loc, start_page, end_page=None):
        """ Add the pages from the source document between the given indices."""
        if end_page == None: # No end page was specified, assume only one page was intended.
            end_page = start_page
        source_file = fitz.open(source_file_loc)
        if end_page == -1: # End on the last page of the document.
            self.doc.insert_pdf(source_file, from_page=start_page) # No to_page argument, default to last page.
        else:
            self.doc.insert_pdf(source_file, from_page=start_page, to_page=end_page)
        source_file.close()
        
    def remove_page(self, page_i):
        """ Remove a page at the given index if it exists. """
        doc_len = len(self.doc) 
        if page_i <= doc_len: # The page exists at the given index.
            new_doc = fitz.open() # Create a new document.
            new_doc.insert_pdf(self.doc, from_page = 0, to_page=page_i-1) # Add all the pages up to the page that is to be removed.
            if page_i != doc_len: # If the page is not the last page...
                new_doc.insert_pdf(self.doc, from_page = page_i+1) # Add all pages after the page to be removed.
            self.doc = new_doc # Replace it with the updated document.
        else: # The page does not exist at the given index.
            raise IndexError(f"Page index out of range for document of length {doc_len}") # Throw an exception.