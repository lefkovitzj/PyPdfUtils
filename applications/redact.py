"""
    Author: AaronTook (https://AaronTook.github.io)
    File Last Modified: 5/8/2024
    Project Name: PySimplePDF
    File Name: applications/redact.py
"""

# Python Standard Library Imports.
import os
import sys
from tkinter import *
from tkinter import filedialog
import traceback
import warnings

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

class Redact_Viewer():
    def __init__(self):
        if len(sys.argv) == 1: # No argument provided, request file path.
            self.file_path = gui_get_file()[0]
            if self.file_path == "":
                sys.exit()
        else: # File path was included as a command-line argument.
            self.file_path = sys.argv[1]
        try:
            self.doc = fitz.open(self.file_path) # Open the PDF.
            page0 = self.doc[0]  # Get the first page, which will be used for window size calculations.
            page0_dimensions = (page0.rect.width, page0.rect.height)
            page = page0
            self.page_i = 0
            self.scale = 1
            
            
            
            # Modfication attributes:
            self.active_start = (None, None)
            self.redactions = [[] for i in range(len(self.doc))]
            self.undone_redactions = [[] for i in range(len(self.doc))]
            
            self.root = ctk.CTk() # Create the GUI window.
            self.screen_height =self. root.winfo_screenheight()
            self.root.title("PDF Viewer")
    
            window_scale = page0_dimensions[1] / self.screen_height
            if window_scale >= 1:
                self.display_height = self.screen_height
                self.display_width = page0_dimensions[0]*(1/window_scale)
            else:
                self.display_height = page0_dimensions[1]
                self.display_width = page0_dimensions[0]
            self.root.geometry(f"{self.display_width}x{self.display_height}")
            self.root.resizable(width=False, height=False) # Prevent the user from changing the width or height of the window.
                        
            # Add the canvas for the pdf and drawings.
            self.pdf_canvas = Canvas(self.root, width = self.display_width, height = self.display_height)
            self.pdf_canvas.pack(anchor='nw', fill='both', expand=1)
            
            # Load the first page.
            self.update_page(0)
            
            
            
            # Event binds.
            self.root.bind("<Left>", self.previous_page)
            self.root.bind("<Right>", self.next_page)
            self.root.bind("<Button-1>", self.set_start)
            self.root.bind("<ButtonRelease-1>", self.set_end)
            self.root.bind("<Control-s>", self.save_pdf_markup)
            self.root.bind("<Control-z>", self.undo)
            self.root.bind("<Control-y>", self.redo)

            # App mainloop.
            self.root.mainloop() # Create the GUI window application.
        
        except Exception: # Handle any application errors by returning them to the user without crashing.
            print(f"Error Message: \"{traceback.format_exc()}\"")
        
    def set_start(self, event): # Add to a click stroke.
        self.active_start = (event.x, event.y)

    def set_end(self, event): # End of a click stroke.
        if (self.active_start[0] != None) and (self.active_start[1] != None):
            rectlike = (self.active_start[0], self.active_start[1], event.x, event.y) # Create and add rect-like (4-value tuple) to redactions.
            self.redactions[self.page_i].append(rectlike) 
            self.active_start = (None, None)
            self.pdf_canvas.create_rectangle(rectlike, fill="black", outline="black")
            self.undone_redactions[self.page_i] = [] # Clear undone redactions, can no longer "undo"
    
    def redraw_page(self, page_num): # Reload all drawings on the page.
        for redactionRectlike in self.redactions[page_num]:
            x1, y1, x2, y2 = redactionRectlike
            self.pdf_canvas.create_rectangle(x1,y1,x2,y2, fill="black", outline="black")
    
    def update_page(self, page_num): # Load the page.
        page = self.doc[page_num]
        pix = page.get_pixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        self.scale = pix.width / (self.display_height) # Calculate and update the scale.

        img.resize((int(pix.width * self.scale), int(pix.height * self.scale))) # Resize and prepare the pdf page image.
        tkimg = ImageTk.PhotoImage(img)
        ctkimg = ctk.CTkImage(light_image=img, dark_image=img, size=(pix.width * self.scale, pix.height * self.scale))
        
        with warnings.catch_warnings(): # Prevent console warning for CTkLabel with non-CTkImage as "image" argument. Solution found at: https://stackoverflow.com/questions/14463277/how-to-disable-python-warnings
            warnings.simplefilter("ignore")
            pic = ctk.CTkLabel(self.pdf_canvas, text="", image = tkimg) # Add the pdf page image.
        self.pdf_canvas.create_image(0,0, image=tkimg, anchor="nw")
        
        self.root.update()
    
    def undo(self, event): # Undo redaction.
        if len(self.redactions[self.page_i]) > 0:
            most_recent = self.redactions[self.page_i][-1]
            self.redactions[self.page_i].pop(-1)
            self.undone_redactions[self.page_i].append(most_recent)
            self.update_page(self.page_i)
            self.redraw_page(self.page_i)

    def redo(self, event): # Redo redaction.
        if len(self.undone_redactions[self.page_i]) > 0:
            most_recent = self.undone_redactions[self.page_i][-1]
            self.undone_redactions[self.page_i].pop(-1)
            self.redactions[self.page_i].append(most_recent)
            self.update_page(self.page_i)
            self.redraw_page(self.page_i)
    
    def next_page(self, *args): # Change the page (+).
        page_i = self.page_i
        if page_i+1 <= len(self.doc)-1:
            self.update_page(page_i+1)
            self.redraw_page(page_i+1)
            self.page_i = page_i+1
            
    def previous_page(self, *args): # Change the page (-).
        page_i = self.page_i
        if page_i-1 >= 0:
            self.update_page(page_i-1)
            self.redraw_page(page_i-1)
            self.page_i = page_i-1

    def save_pdf_markup(self, event): # Save the modified pdf document.
        for page_i in range(len(self.doc)):
            page = self.doc[page_i]
            redactions = self.redactions[page_i]
            for redaction_rectlike in redactions:
                page.add_redact_annot(redaction_rectlike, fill=(0,0,0))
            page.apply_redactions()
            
        self.doc.save(f"{self.file_path} - edited.pdf")
        self.root.destroy()

if __name__ == "__main__":
    app = Redact_Viewer()