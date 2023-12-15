import threading
from tkinter import ttk, filedialog, messagebox
import tkinter as tk

from add_project import add_project
from gui.input_validator import Properties, validate, is_api_type_set
from gui.llama_index_init import init_llama_index


class ProjectsTab:
    def __init__(self, root, frame):
        self.frame = frame
        self.root = root

        # Select Directory
        ttk.Label(frame, text="Project Directory:").grid(column=0, row=0, sticky='W')
        self.select_directory_button = ttk.Button(frame, text="Select Directory",
                                                  command=self.select_directory)
        self.select_directory_button.grid(column=1, row=0, padx=5, pady=5)

        # Project Name
        ttk.Label(frame, text="Project Name:").grid(column=0, row=1, sticky='W')
        self.project_name_entry = ttk.Entry(frame, width=90)
        self.project_name_entry.grid(column=1, row=1, padx=5, pady=5)

        # Ignore List
        ttk.Label(frame, text="Files to ignore:").grid(column=0, row=2, sticky='NW')
        # Frame for Listbox and scrollbars
        self.ignore_listbox_frame = tk.Frame(frame)
        self.ignore_listbox_frame.grid(column=1, row=2, padx=5, pady=5, sticky='nsew')

        # Vertical scrollbar
        self.ignore_vscrollbar = tk.Scrollbar(self.ignore_listbox_frame, orient='vertical')
        self.ignore_vscrollbar.pack(side='right', fill='y')

        # Horizontal scrollbar
        self.ignore_hscrollbar = tk.Scrollbar(self.ignore_listbox_frame, orient='horizontal')
        self.ignore_hscrollbar.pack(side='bottom', fill='x')

        # Ignore Listbox
        self.ignore_listbox = tk.Listbox(self.ignore_listbox_frame, height=5, width=90,
                                         yscrollcommand=self.ignore_vscrollbar.set,
                                         xscrollcommand=self.ignore_hscrollbar.set)
        self.ignore_listbox.pack(side='left', fill='both', expand=True)

        # Configure scrollbars
        self.ignore_vscrollbar.config(command=self.ignore_listbox.yview)
        self.ignore_hscrollbar.config(command=self.ignore_listbox.xview)

        # Frame for buttons
        self.buttons_frame = tk.Frame(frame)
        self.buttons_frame.grid(column=1, row=3, padx=5, pady=5, sticky='w')

        # Select Files Button
        self.select_files_button = ttk.Button(self.buttons_frame, text="Select", command=self.select_files)
        self.select_files_button.grid(column=0, row=0)
        ttk.Label(self.buttons_frame, text="Select which files should be ignored while indexing").grid(column=0, row=1,
                                                                                                       sticky='NW')

        # Spacer frame to create gap between buttons
        self.spacer_frame = tk.Frame(self.buttons_frame, width=40)
        self.spacer_frame.grid(column=1, row=0)

        # Delete Selected File Button
        self.delete_file_button = ttk.Button(self.buttons_frame, text="Delete", command=self.delete_selected_file)
        self.delete_file_button.grid(column=2, row=0)
        ttk.Label(self.buttons_frame, text="Remove selected file from the list").grid(column=2, row=1, sticky='NW')

        # Add new Project Button
        self.execute_action_button = ttk.Button(frame, text="Create Index",
                                                command=self.add_new_project, style='W.TButton')
        self.execute_action_button.grid(column=1, row=4, padx=5, pady=5)

        self.generating_label = ttk.Label(frame, text="")
        self.generating_label.grid(column=1, row=5, padx=5, pady=5)

        # Project List Area
        ttk.Label(frame, text="Selected Project:").grid(column=0, row=6, sticky='NW')
        self.selected_project = ttk.Combobox(frame, width=88)
        self.selected_project.grid(column=1, row=6, padx=5, pady=5)

        # Logs
        ttk.Label(frame, text="Logs:").grid(column=0, row=7, sticky='NW')
        # Frame for Logs
        self.logs_frame = tk.Frame(frame)
        self.logs_frame.grid(column=1, row=8, padx=5, pady=5, sticky='nsew')

        # Vertical scrollbar
        self.logs_vscrollbar = tk.Scrollbar(self.logs_frame, orient='vertical')
        self.logs_vscrollbar.pack(side='right', fill='y')

        # Horizontal scrollbar
        self.logs_hscrollbar = tk.Scrollbar(self.logs_frame, orient='horizontal')
        self.logs_hscrollbar.pack(side='bottom', fill='x')

        # Logs Listbox
        self.logs_listbox = tk.Listbox(self.logs_frame, height=5, width=90,
                                       yscrollcommand=self.logs_vscrollbar.set,
                                       xscrollcommand=self.logs_hscrollbar.set)
        self.logs_listbox.pack(side='left', fill='both', expand=True)

        # Configure scrollbars
        self.logs_vscrollbar.config(command=self.logs_listbox.yview)
        self.logs_hscrollbar.config(command=self.logs_listbox.xview)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.selected_directory = directory
            self.select_directory_button.config(text=f"Directory: {directory}")

    def select_files(self):
        if hasattr(self, 'selected_directory'):
            files = filedialog.askopenfilenames(initialdir=self.selected_directory, title="Select Files",
                                                filetypes=(("All files", "*.*"),))
            for file in files:
                if file not in self.ignore_listbox.get(0, tk.END):  # Avoid duplicates
                    self.ignore_listbox.insert(tk.END, file)
        else:
            messagebox.showerror("Error", "Please select a directory first.")

    def delete_selected_file(self):
        selected_items = self.ignore_listbox.curselection()
        # Must delete from the end to avoid shifting of the indices
        for i in reversed(selected_items):
            self.ignore_listbox.delete(i)

    def add_new_project(self):
        if not is_api_type_set(self.root):
            return

        is_valid = validate(self.root, [
            Properties.PROJECT_NAME,
            Properties.SELECTED_DIRECTORY,
            Properties.API_TYPE,
        ])

        if not is_valid:
            return

        project_name = self.project_name_entry.get()
        directory = self.selected_directory
        files = self.ignore_listbox.get(0, tk.END)
        api_type = self.root.settings_tab.api_type.get()

        init_llama_index(self.root, api_type)

        self.generating_label.config(text="Generating index, please wait...")

        thread = threading.Thread(target=add_project, args=(
            self.root,
            directory,
            project_name,
            files,
        ))

        thread.start()

