import threading
from tkinter import ttk, filedialog, messagebox
import tkinter as tk

from helpers.add_project import add_project
from gui.input_validator import Properties, validate, is_api_type_set
from gui.llama_index_init import init_llama_index


class ProjectsTab:
    def __init__(self, root, frame):
        self.frame = frame
        self.root = root

        # Select Directory
        ttk.Label(frame, text="Project Directory:", style='W.Label').pack(fill=tk.X, padx=10, pady=(12, 2))
        self.select_directory_button = ttk.Button(frame, text="Select Directory",
                                                  command=self.select_directory)
        self.select_directory_button.pack(padx=10, pady=10)

        # Project Name
        ttk.Label(frame, text="Project Name:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        self.project_name_entry = ttk.Entry(frame)
        self.project_name_entry.pack(fill=tk.X, padx=10, pady=10)

        # Ignore List
        ttk.Label(frame, text="Files to ignore:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        # Frame for Listbox and scrollbars
        self.ignore_listbox_frame = tk.Frame(frame)
        self.ignore_listbox_frame.pack(fill=tk.X, padx=10, pady=10)

        # Vertical scrollbar
        self.ignore_vscrollbar = tk.Scrollbar(self.ignore_listbox_frame, orient='vertical')
        self.ignore_vscrollbar.pack(side='right', fill='y')

        # Ignore Listbox
        self.ignore_listbox = tk.Listbox(self.ignore_listbox_frame, height=5,
                                         yscrollcommand=self.ignore_vscrollbar.set)
        self.ignore_listbox.pack(side='left', fill='both', expand=True)

        # Configure scrollbars
        self.ignore_vscrollbar.config(command=self.ignore_listbox.yview)

        # Frame for buttons
        self.buttons_frame = tk.Frame(frame)
        self.buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        # Select Files Button
        self.select_files_button = ttk.Button(self.buttons_frame, text="Select", command=self.select_files)
        self.select_files_button.pack(side='left', padx=5, pady=5)
        ttk.Label(self.buttons_frame, text="Select which files should be ignored while indexing")\
            .pack(side='left', padx=10, pady=2)

        # Spacer frame to create gap between buttons
        self.spacer_frame = tk.Frame(self.buttons_frame, width=40)
        self.spacer_frame.pack(side='left', padx=5, pady=5)

        # Delete Selected File Button
        self.delete_file_button = ttk.Button(self.buttons_frame, text="Delete", command=self.delete_selected_file)
        self.delete_file_button.pack(side='left', padx=5, pady=5)
        ttk.Label(self.buttons_frame, text="Remove selected file from the list").pack(side='left', padx=10, pady=2)

        # Ignore Directory List
        ttk.Label(frame, text="Directories to ignore:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        # Frame for Listbox and scrollbars
        self.ignore_directory_listbox_frame = tk.Frame(frame)
        self.ignore_directory_listbox_frame.pack(fill=tk.X, padx=10, pady=10)

        # Vertical scrollbar
        self.ignore_directory_vscrollbar = tk.Scrollbar(self.ignore_directory_listbox_frame, orient='vertical')
        self.ignore_directory_vscrollbar.pack(side='right', fill='y')

        # Ignore Listbox
        self.ignore_directory_listbox = tk.Listbox(self.ignore_directory_listbox_frame, height=5,
                                         yscrollcommand=self.ignore_directory_vscrollbar.set)
        self.ignore_directory_listbox.pack(side='left', fill='both', expand=True)

        # Configure scrollbars
        self.ignore_directory_vscrollbar.config(command=self.ignore_directory_listbox.yview)

        # Frame for buttons
        self.buttons_directory_frame = tk.Frame(frame)
        self.buttons_directory_frame.pack(fill=tk.X, padx=10, pady=10)

        # Select Files Button
        self.select_directories_button = ttk.Button(self.buttons_directory_frame, text="Select",
                                                    command=self.select_ignored_directory)
        self.select_directories_button.pack(side='left', padx=5, pady=5)
        ttk.Label(self.buttons_directory_frame, text="Select which directories should be ignored while indexing") \
            .pack(side='left', padx=10, pady=2)

        # Spacer frame to create gap between buttons
        self.spacer_directories_frame = tk.Frame(self.buttons_directory_frame, width=40)
        self.spacer_directories_frame.pack(side='left', padx=5, pady=5)

        # Delete Selected File Button
        self.delete_directory_button = ttk.Button(self.buttons_directory_frame, text="Delete",
                                                  command=self.delete_selected_directory)
        self.delete_directory_button.pack(side='left', padx=5, pady=5)
        ttk.Label(self.buttons_directory_frame, text="Remove selected directory from the list").pack(side='left', padx=10, pady=2)

        # Add new Project Button
        self.execute_action_button = ttk.Button(frame, text="Create Index",
                                                command=self.add_new_project, style='W.TButton')
        self.execute_action_button.pack(padx=10, pady=10)

        self.generating_label = ttk.Label(frame, text="")
        self.generating_label.pack(padx=10, pady=10)

        # Project List Area
        ttk.Label(frame, text="Selected Project:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        self.selected_project = ttk.Combobox(frame)
        self.selected_project.pack(fill=tk.X, padx=10, pady=10)

        # Logs
        ttk.Label(frame, text="Logs:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        # Frame for Logs
        self.logs_frame = tk.Frame(frame)
        self.logs_frame.pack(fill=tk.X, padx=10, pady=10)

        # Vertical scrollbar
        self.logs_vscrollbar = tk.Scrollbar(self.logs_frame, orient='vertical')
        self.logs_vscrollbar.pack(side='right', fill='y')

        # Logs Listbox
        self.logs_listbox = tk.Listbox(self.logs_frame, height=8,
                                       yscrollcommand=self.logs_vscrollbar.set)
        self.logs_listbox.pack(side='left', fill='both', expand=True)

        # Configure scrollbars
        self.logs_vscrollbar.config(command=self.logs_listbox.yview)

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

    def select_ignored_directory(self):
        if hasattr(self, 'selected_directory'):
            directory = filedialog.askdirectory(initialdir=self.selected_directory, title="Select Directory")
            if directory:
                if directory not in self.ignore_directory_listbox.get(0, tk.END):
                    self.ignore_directory_listbox.insert(tk.END, directory)

    def delete_selected_directory(self):
        selected_items = self.ignore_directory_listbox.curselection()
        # Must delete from the end to avoid shifting of the indices
        for i in reversed(selected_items):
            self.ignore_directory_listbox.delete(i)

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
        directories = self.ignore_directory_listbox.get(0, tk.END)
        api_type = self.root.settings_tab.api_type.get()

        init_llama_index(self.root, api_type)

        self.generating_label.config(text="Generating index, please wait...")

        try:
            thread = threading.Thread(target=add_project, args=(
                self.root,
                directory,
                project_name,
                files,
                directories,
            ))

            thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Error while generating index!")
            self.generating_label.config(text="Finished!")
            self.logs_listbox.insert(tk.END, f"Error: {e}")

