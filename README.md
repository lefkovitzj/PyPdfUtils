# PyPdfUtils
A PDF manipulation and access toolkit developed in Python using the PyMuPDF module.

This repository is home to various smaller PDF-related projects that will hopefully be combined eventually to form one application. Not all files are meant to be run independently, but a list of files that can be run by themselves is included below. Some files are copies or modified versions of my other projects, with links provided here to find the original.

----------------------------
Project Requirements (cumulative for all files):
  1. Must have the following Third-party Modules installed:
      <br>PyMuPDF (https://pymupdf.readthedocs.io/en/latest/index.html)
      <br>CustomTkinter (https://customtkinter.tomschimansky.com/documentation/)
      <br>Pillow (https://pillow.readthedocs.io/en/stable/)
  3. Must have access to the following Python Standard Library modules:
      <br>os
      <br>tkinter
      <br>sys
      <br>datetime
----------------------------

Current Project Files:
<br>applications/viewer.py: This file is a copy of a simple PDF viewer that I created recently (original code: https://github.com/AaronTook/PySimplePDF). When a GUI application for all functionality is later created, my intention is to use it to preview documents before deciding to save them.
<br>operations/merge.py: This file contains a class that can be used to create objects which represent a file to have pages added or removed. This functionality essentially merges various portions of any number of PDFs together to produce a desired result.
<br>operations/encryption.py: This file contains functions that can be used to create encrypted and decrypted versions of PDF files.
<br>operations/compression.py: This file will contain functionality for file compression.

----------------------------

Future Project Plans:
<br>applications/markup.py: This file will run an application like viewer.py, but with the ability to add text overlays to each page of a PDF.
<br>operations/extract.py: This file will contain functions to extract images or text from a PDF.
<br>operations/watermark.py: This file will contain the functions to add a watermark to each page of a PDF document.
<br>app.py: The end goal of this project is to have one GUI application that allows the user to use each of the operations or launch any of the applications listed seperately. It will also allow a license agreement on the first launch and will check for updates to the software when an internet connection is available.

----------------------------

Many thanks to the developers and contributors of the PyMuPDF, CustomTkinter and Pillow projects, without whose work this project would not have been possible. 
