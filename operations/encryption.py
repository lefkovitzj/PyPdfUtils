"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 2/26/2024
    Project Name: PyPdfUtils
    File Name: operations/encryption.py
"""

import fitz
import datetime
import os

def calculate_pdf_temp_title(action):
    tb = str(datetime.datetime.today()) # Basic timestamp string, with the type of action included.
    file_title = tb[:4] + "-" + tb[5:7] + "-" + tb[8:10] + "_" + tb[11:13] + "-" + tb[14:16] + "-" + tb[17:19] + "_" + action + "_" + ".pdf"
    return file_title

class PDF_Crypter():
    def __init__(self, fitz_doc):
        """ Initialize the object. """
        if "temporary_files" not in os.listdir(os.getcwd()): # Ensure that the necessary save folder exists.
            os.makedirs("temporary_files") 
        self.doc = fitz_doc
    def is_encrypted_file(self):
        """ Returns true if the file is currently encrypted. """
        return bool(self.doc.needs_pass)
    def is_encrypted(self):
        """ Returns true if the document instance is currently encrypted. """
        return self.doc.is_encrypted
    def decrypt(self, password):
        """ Create a copy of the file which has been decrypted. """
        if self.is_encrypted(): # Ensure that the file is encrypted.
            decryption_status = self.doc.authenticate(password)
        else: # The file is not encrypted.
            return False, "File is not encrypted"
        self.doc.save("temporary_files\\" + calculate_pdf_temp_title("decrypt"))  # Save a copy of the document.
        return True os.getcwd() + "temporary_files\\" + calculate_pdf_temp_title("decrypt") # Return the file path of the file copy.
    def encrypt(self, password, owner_password=None):
        """ Create a copy of the file which has been encrypted. """
        if not self.is_encrypted(): # Ensure that the file is not encrypted.
            perm = int( # Set the permissions for the file.
                fitz.PDF_PERM_ACCESSIBILITY
                | fitz.PDF_PERM_PRINT
                | fitz.PDF_PERM_COPY
                | fitz.PDF_PERM_ANNOTATE
            )
            if owner_password == None: # If no owner password is set, use the same as the user password.
                owner_password = password
            owner_pass = owner_password
            user_pass = password
            encrypt_meth = fitz.PDF_ENCRYPT_AES_256 # Use the strongest algorithm available.
            
            self.doc.save("temporary_files\\" + calculate_pdf_temp_title("encrypt"), encryption=encrypt_meth, owner_pw=owner_pass, user_pw=user_pass, permissions=perm) # Save a copy of the document.
        else: # The file is encrypted.
            return False, "File is encrypted."
        return True, os.getcwd() + "temporary_files\\" + calculate_pdf_temp_title("encrypt") # Return the file path of the file copy.
