import json
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, ttk
import os
import subprocess
import sys

# Define the base folder to run searches in
base_folder = r'\\my_server\my_share_name'

class PDFSearchApp:
    def __init__(self, root, base_folder):
        self.root = root
        root.title('Find Files')

        self.base_folder = base_folder

        # Folder selection
        folder_frame = tk.Frame(root)
        folder_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(folder_frame, text='Journal Type:').pack(side=tk.LEFT)

        # Fetch subdirectories and populate the dropdown
        self.folder_var = tk.StringVar()
        self.folders = self.get_directories(base_folder)
        self.folder_dropdown = ttk.Combobox(folder_frame, textvariable=self.folder_var, values=self.folders,
                                            state='readonly')
        self.folder_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)
        if self.folders:
            self.folder_dropdown.current(0)
        self.folder_dropdown.bind('<<ComboboxSelected>>', self.on_folder_select)  # Clear listbox on new selection

        # Search text input
        search_frame = tk.Frame(root)
        search_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(search_frame, text='Search For:').pack(side=tk.LEFT)
        self.search_text_entry = tk.Entry(search_frame, width=50)
        self.search_text_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_text_entry.bind("<Return>", self.trigger_search)  # Bind Enter key to search

        self.search_button = tk.Button(search_frame, text='Search', command=self.search_in_index)
        self.search_button.pack(side=tk.RIGHT, padx=10)

        # Listbox with a scrollbar
        listbox_frame = tk.Frame(root)
        listbox_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.listbox = Listbox(listbox_frame, width=100, height=15)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(listbox_frame, orient="vertical")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)

    def get_directories(self, path):
        """Retrieve a list of subdirectories under the specified path."""
        directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        return directories

    def on_folder_select(self, event):
        # Clear the listbox when a new folder is selected
        self.listbox.delete(0, tk.END)

    def search_in_index(self, event=None):
        self.listbox.delete(0, tk.END)
        selected_folder = self.folder_var.get()
        folder_path = os.path.join(self.base_folder, selected_folder)
        search_text = self.search_text_entry.get()
        index_file = os.path.join(folder_path, 'index.json')

        if not os.path.exists(index_file):
            messagebox.showerror("Error", "Index file not found. Please create the index first.")
            return

        if search_text and selected_folder:
            try:
                with open(index_file, 'r') as f:
                    index = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the index file: {e}")
                return

            matching_pdfs = [filename for filename, text in index.items() if search_text.lower() in text.lower()]

            for item in matching_pdfs:
                self.listbox.insert(tk.END, item)

            if not matching_pdfs:
                messagebox.showinfo("Search Complete", "No matches found.")

    def trigger_search(self, event):
        self.search_in_index()

    def on_listbox_select(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            pdf_file = widget.get(index)
            selected_folder = self.folder_var.get()
            pdf_path = os.path.join(self.base_folder, selected_folder, pdf_file)
            self.open_pdf(pdf_path)

    def open_pdf(self, pdf_path):
        if sys.platform == "win32":
            os.startfile(pdf_path)
        elif sys.platform == "darwin":
            subprocess.call(["open", pdf_path])


# Specify the base folder where the directories are located
root = tk.Tk()
app = PDFSearchApp(root, base_folder)
root.mainloop()
