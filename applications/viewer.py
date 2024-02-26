"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 2/25/2024
    Project Name: PyPdfUtils
    File Name: applications/viewer.py
"""

# Python Standard Library Imports.
import os
import sys
from tkinter import *
from tkinter import filedialog

# Third-party Module Imports.
from PIL import Image, ImageTk
import fitz
import customtkinter as ctk


def gui_get_file(initial_directory="", limit_filetypes=[]): 
    """ Open file explorer (using tkinter) to select a file. """
    root = Tk() # Create the GUI window.
    root.withdraw()
    complete_file_path = filedialog.askopenfilename(title="File Select", initialdir = os.getcwd() + "/" + initial_directory, filetypes = limit_filetypes) # Select the file.
    root.destroy()
    file_path, file_name = os.path.split(complete_file_path) # Get the filepath and filename to return to the user.
    return complete_file_path, file_name

def calculate_from_pdf_timestamp(pdf_timestamp): 
    """ Reformat the PDF Timestamp in the format used to store PDF metadata. """
    assert pdf_timestamp.startswith("D:")
    year = pdf_timestamp[2 : 6] # YYYY
    month = pdf_timestamp[7 : 8] # MM
    day= pdf_timestamp[8 : 10] # DD
    hour = pdf_timestamp[10 : 12] # hh
    minute = pdf_timestamp[12 : 14] # mm
    seconds = pdf_timestamp[14 : 16]# ss
    tz = pdf_timestamp[16 : ]
    tz_hour_diff = tz[1 : 3]
    tz_sign = tz[0]
    tz_min_diff = tz[4 : 6]
    am_pm = "AM" if (int(hour)<12 or int(hour)==24) else "PM (UTC)" # Calculate the time for a 12-hour clock.
    hour = int(hour)-12 if int(hour) > 12 else int(hour) 
    return f"{month}/{day}/{year} at {hour}:{minute} {am_pm}" # Return the reformatted data.

if __name__ == "__main__":
    if len(sys.argv) == 1: # No argument provided, request file path.
        file_path = gui_get_file()[0]
        if file_path == "":
            sys.exit()
    else: # File path was included as a command-line argument.
        file_path = sys.argv[1]
    try:
        doc = fitz.open(file_path) # Open the PDF.
        page0 = doc[0]  # Get the first page, which will be used for window size calculations.
        page0_dimensions = (page0.rect.width, page0.rect.height)
        page = page0
        
        last_mod_time = calculate_from_pdf_timestamp(doc.metadata["modDate"]) # Get the date that the file was last modified from the metadata.
        
        root = ctk.CTk() # Create the GUI window.
        screen_height = root.winfo_screenheight()
        root.title("PDF Viewer")

        display_height = (screen_height if screen_height < page0_dimensions[1] else page0_dimensions[1])*0.8 # Calculate the window height at 80% of the page or screen, whichever is smaller.
        root.resizable(width=False, height=True) # Prevent the user from changing the width of the window.
        
        display_message = ctk.CTkLabel(root, text=f"File path: {os.path.split(file_path)[1]}\nLast modified: {last_mod_time}", anchor="w", width = page0_dimensions[0], justify="left")
        display_message.pack() # Add a message with file details to the window.
        
        pdf_frame = ctk.CTkScrollableFrame(master = root, width = page0_dimensions[0], height = display_height) # Create and configure a frame to hold the PDF page images.
        pdf_frame.grid_rowconfigure(0, weight=1)
        pdf_frame.grid_columnconfigure(0, weight=1)
        
        for page_i in range(len(doc)): # Iterate through each page in the PDF.
            page = doc[page_i]
            pix = page.get_pixmap() # Convert the page to an image to be placed in the frame.
            # set the mode depending on alpha
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            ctkimg = ctk.CTkImage(light_image=img,
                                                dark_image=img, 
                                                size = (pix.width, pix.height))
            
            ctk.CTkLabel(pdf_frame, text="", image=ctkimg,).grid(row=page_i*2, column=0) # Add the image to the CTkScrollableFrame.
            if page_i != len(doc)-1: # The page is not the last page, add a regular separator.
                ctk.CTkLabel(pdf_frame, text=f"- End Page {page_i+1} -", pady= 10).grid(row=page_i*2 + 1, column=0)
            else: # It is the last page, add the end of document separator.
                ctk.CTkLabel(pdf_frame, text=f"- End of Document -", pady= 10).grid(row=page_i*2 + 1, column=0)
        pdf_frame.pack()
        
        root.mainloop() # Create the GUI window application.
    
    except Exception as e: # Handle any application errors by returning them to the user without crashing.
        print(f"Error Message: \"{e}\"")
