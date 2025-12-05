""" Hooks for right key to combine

# Create menu entry for PDFs
New-Item -Path "Registry::HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CombinePDFs" -Force | Out-Null

# Set menu text
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CombinePDFs" `
    -Name "MUIVerb" -Value "Combine PDFs" -Force

# Optional: give it an icon
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CombinePDFs" `
    -Name "Icon" -Value "explorer.exe" -Force

# Create command subkey
New-Item -Path "Registry::HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CombinePDFs\command" -Force | Out-Null

# Wire the command to your .bat launcher
Set-ItemProperty -Path "Registry::HKEY_CLASSES_ROOT\SystemFileAssociations\.pdf\shell\CombinePDFs\command" `
    -Name "(Default)" `
    -Value '"C:\Tools\merge_pdfs_gui.bat"' -Force

"""

import sys
import tkinter as tk
from tkinter import filedialog, messagebox

from pypdf import PdfReader, PdfWriter  # works on new pypdf

def main():
    root = tk.Tk()
    root.withdraw()  # hide main window

    # --- select PDFs ---
    filepaths = filedialog.askopenfilenames(
        title="Select PDF files to combine",
        filetypes=[("PDF files", "*.pdf")],
    )
    if not filepaths or len(filepaths) < 2:
        messagebox.showinfo("Combine PDFs", "Please select at least two PDF files.")
        return

    # Optional: sort by filename. Remove this if you want the raw selection order.
    filepaths = sorted(filepaths)

    # --- choose output file ---
    out_path = filedialog.asksaveasfilename(
        title="Save merged PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        initialfile="merged.pdf",
    )
    if not out_path:
        return

    # --- merge ---
    writer = PdfWriter()

    try:
        for path in filepaths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)

        with open(out_path, "wb") as f:
            writer.write(f)

        messagebox.showinfo(
            "Combine PDFs",
            f"Merged {len(filepaths)} files into:\n{out_path}",
        )
    except Exception as e:
        messagebox.showerror("Combine PDFs - Error", f"Error while merging:\n{e}")

if __name__ == "__main__":
    main()
