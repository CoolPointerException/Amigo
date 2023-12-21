import threading
from tkinter import ttk, filedialog, messagebox
import tkinter as tk

from helpers.add_project import add_project, git_diff
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
        ttk.Label(frame, text="Reindex Project:", style='W.Label').pack(fill=tk.X, padx=10, pady=2)
        ttk.Label(frame, text="In case there is a .git folder in your root directory, you have an option to reindex "
                              "only the files that were added or modified since the last indexing.", wraplength=880)\
            .pack(fill=tk.X, padx=10, pady=2)

        self.reindex_frame = tk.Frame(frame)
        self.reindex_frame.pack(fill=tk.X)

        self.reindex_project = ttk.Combobox(self.reindex_frame)
        self.reindex_project.pack(side='left', padx=10, pady=10, fill=tk.X, expand=True)

        # Add new Project Button
        self.reindex_project_button = ttk.Button(self.reindex_frame, text="Reindex", command=self.reindex_project_action)
        self.reindex_project_button.pack(side='left', padx=10, pady=10)

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

    def reindex_project_action(self):
        is_valid = validate(self.root, [
            Properties.REINDEX_PROJECT,
            Properties.THREADS,
        ])

        if not is_valid:
            return

        reindex_project = self.reindex_project.get()

        # parse project name and project directory
        reindex_project = reindex_project.split(" | ")
        project_name = reindex_project[0]
        project_dir = reindex_project[1]

        f = open(project_name + "/ignored_files.txt", "r")
        ignored_files = f.read().split("\n")

        f = open(project_name + "/ignored_directories.txt", "r")
        ignored_directories = f.read().split("\n")

        self.create_index_project(
            project_name,
            project_dir,
            ignored_files,
            ignored_directories,
            True
        )

    def add_new_project(self):
        is_valid = validate(self.root, [
            Properties.PROJECT_NAME,
            Properties.SELECTED_DIRECTORY,
            Properties.THREADS,
        ])

        if not is_valid:
            return

        project_name = self.project_name_entry.get()
        directory = self.selected_directory
        files = self.ignore_listbox.get(0, tk.END)
        directories = self.ignore_directory_listbox.get(0, tk.END)

        self.create_index_project(
            project_name,
            directory,
            files,
            directories,
        )

    def create_index_project(
            self,
            project_name,
            directory,
            files,
            directories,
            is_reindex=False
    ):
        if not is_api_type_set(self.root):
            return

        api_type = self.root.settings_tab.api_type.get()
        threads = int(self.root.settings_tab.threads.get())

        init_llama_index(self.root, api_type)

        diff = None
        if is_reindex:
            diff = git_diff(project_name, self.root)

        self.generating_label.config(text="Generating index, please wait...")

        try:
            thread = threading.Thread(target=add_project, args=(
                self.root,
                directory,
                project_name,
                files,
                directories,
                is_reindex,
                diff,
                threads
            ))

            thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Error while generating index!")
            self.generating_label.config(text="Finished!")
            self.logs_listbox.insert(tk.END, f"Error: {e}")

