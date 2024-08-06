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
<ul>
  <li>applications/viewer.py: This file is a copy of a simple PDF viewer that I created recently (original code: https://github.com/lefkovitzj/PySimplePDF). When a GUI application for all functionality is later created, my intention is to use it to preview documents before deciding to save them.</li>
  <li>applications/draw.py: This file enables the user to "draw" on each page of a PDF with a mouse (or other available input methods).</li>
  <li>applications/redact.py: This file enables the user to redact rectangles of information on each page of a PDF with a mouse (or other available input methods).</li>
  <li>operations/merge.py: This file contains a class that can be used to create objects which represent a file to have pages added or removed. This functionality essentially merges various portions of any number of PDFs together to produce a desired result.</li>
  <li>operations/encryption.py: This file contains functions that can be used to create encrypted and decrypted versions of PDF files.</li>
  <li>operations/compression.py: This file contains functionality for file compression.</li>
  <li>operations/extract.py: This file contains functions to extract images or text from a PDF.</li>
  <li>operations/watermark.py: This file contains the functions to add a watermark to each page of a PDF document.</li>
</ul>

----------------------------

Future Project Plans:
<ul>
  <li>applications/markup.py: This file will run an application like viewer.py, but with the ability to add text overlays to each page of a PDF.</li>
  <li>app.py: The end goal of this project is to have one GUI application that allows the user to use each of the operations or launch any of the applications listed seperately. It will also allow a license agreement on the first launch and will check for updates to the software when an internet connection is available.</li>
</ul>

----------------------------

Many thanks to the developers and contributors of the PyMuPDF, CustomTkinter and Pillow projects, without whose work this project would not have been possible. 
