import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import ghostscript as gs
from pathlib import Path


class MainApp(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.parent = parent

    # File select button
    self.file_select_button = tk.Button(master=parent, text="Select file", command=self.open_file_select)
    self.file_select_button.pack()

    # Label which shows the selected file
    self.file_path = "No file selected"
    self.file_path_label = tk.Label(text=self.file_path)
    self.file_path_label.pack()

    # Value entered here will be used as ColorImageResolution, GrayImageResolution and MonoImageResolution
    self.resolution_field = tk.Entry(master=parent)
    self.resolution_field.pack()
    self.resolution_field.insert(144, "144")  # Default value

    self.compress_button = tk.Button(master=parent, text="Compress", command=self.compress_pdf)
    self.compress_button.pack()

  # Function to show file select dialog
  def open_file_select(self):
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )

    self.file_path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    if self.file_path == "":
      self.file_path = "No file selected"

    showinfo(
        title='Selected File',
        message=self.file_path
    )

    self.file_path_label.config(text=self.file_path)

  def compress_pdf(self):
    if (self.file_path == "No file selected"):
        return showinfo(
          title="Error",
          message="No file selected"
        )

    if (self.resolution_field.get() == ""):
        return showinfo(
          title="Error",
          message="No value for resolution entered"
        )

    # Select folder to save file
    save_folder = fd.askdirectory(
      title="Select a folder to save the compressed file"
    )

    # Get file name from file path(with extension)
    file_name = os.path.basename(self.file_path)
    # Remove extension from file name
    file_name = os.path.splitext(file_name)[0]
    
    args = [
      "-q", "-dNOPAUSE", "-dBATCH", "-dSAFER",
      "-sDEVICE=pdfwrite",
      "-dCompatibilityLevel=1.3",
      "-dPDFSETTINGS=/screen",
      "-dEmbedAllFonts=true", "-dSubsetFonts=true",
      "-dColorImageDownsampleType=/Bicubic",
      f"-dColorImageResolution={self.resolution_field.get()}",
      "-dGrayImageDownsampleType=/Bicubic",
      f"-dGrayImageResolution={self.resolution_field.get()}",
      "-dMonoImageDownsampleType=/Bicubic",
      f"-dMonoImageResolution={self.resolution_field.get()}",
      f"-sOutputFile={save_folder}/{file_name}-Compressed.pdf",
      self.file_path,
    ]

    file_size = Path(self.file_path).stat().st_size

    try:
      gs.Ghostscript(*args)

      showinfo(
        title="Success",
        message=f"File size after compression: {sizeof_fmt(file_size)}"
      )
    except:
      showinfo(
        title="Error",
        message="Unable to compress file!"
      )


# Function to convert bytes into human readable file sizes
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.00:
            return f"{num:3.2f}{unit}{suffix}"
        num /= 1024.00
    return f"{num:.2f}Yi{suffix}"


if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("350x200")
  MainApp(root).pack(side="top", fill="both", expand=True)
  root.mainloop()
