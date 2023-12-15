import os
import tempfile
from tkinter import ttk, scrolledtext
import tkinter as tk

from gui.input_validator import Properties, validate
from gui.llama_index_init import init_llama_index
from question import question
from tkinterweb import HtmlFrame


class TaskTab:
    def __init__(self, root, frame):
        self.frame = frame
        self.root = root

        # Task Requirements
        ttk.Label(frame, text="Task Requirements:").grid(column=0, row=0, sticky='W')
        self.task_requirements_entry = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=5)
        self.task_requirements_entry.configure(state='normal')
        self.task_requirements_entry.grid(column=1, row=0, padx=5, pady=5, rowspan=5)

        # Run Generation Button
        self.run_generation_button = ttk.Button(frame, text="Run Generation", command=self.generate_answer)
        self.run_generation_button.grid(column=1, row=6, padx=5, pady=5)

        # Generation Response Field
        self.generation_response_frame = ttk.Frame(self.frame, width=80, height=25)
        self.generation_response_frame.grid(column=0, row=7, columnspan=2, padx=5, pady=5)
        self.generation_response = HtmlFrame(self.generation_response_frame)

    def generate_answer(self):
        is_valid = validate(self.root, [
            Properties.TASK_REQUIREMENTS,
            Properties.SELECTED_PROJECT,
            Properties.PROMPT,
            Properties.MAX_TOKENS,
            Properties.API_TYPE,
        ])
        if not is_valid:
            return

        api_type = self.root.settings_tab.api_type.get()
        task_requirements = self.task_requirements_entry.get("1.0", tk.END)
        project_name = self.root.projects_tab.selected_project.get()
        prompt = self.root.settings_tab.prompt_entry.get("1.0", tk.END)
        max_tokens = self.root.settings_tab.max_tokens.get()

        init_llama_index(self.root, api_type)

        try:
            response = question(
                project_name,
                task_requirements,
                prompt,
                max_tokens,
                self.root
            )

            self.load_web_page(response)
        except Exception as e:
            self.load_web_page(str(e))

    def load_web_page(self, text):
        text = text.replace("\n", "<br>")
        tempfile.NamedTemporaryFile(mode='w')
        f = open("temp.html", 'w')
        f.write(f"<html><body>{text}</body></html>")
        f.flush()
        f.close()
        self.generation_response.load_file(os.path.abspath(f.name), force=True)
        self.generation_response.pack()
        return True
