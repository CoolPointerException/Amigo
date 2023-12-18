import os
import tempfile
import threading
from tkinter import ttk, scrolledtext, messagebox
import tkinter as tk

from llama_index.llms import ChatMessage

from gui.input_validator import Properties, validate
from gui.llama_index_init import init_llama_index
from helpers.question import question
from tkinterweb import HtmlFrame


class TaskTab:
    def __init__(self, root, frame):
        self.frame = frame
        self.root = root

        # Task Requirements
        ttk.Label(frame, text="Task Requirements:", style='W.Label').pack(fill=tk.X, padx=10, pady=(12, 2))
        self.task_requirements_entry = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=7)
        self.task_requirements_entry.configure(state='normal')
        self.task_requirements_entry.pack(fill=tk.X, padx=10, pady=10)

        # Run Generation Button
        self.run_generation_button = ttk.Button(frame, text="Generate", command=self.generate_answer)
        self.run_generation_button.pack(padx=10, pady=10)

        # Clear chat Button
        self.run_generation_button = ttk.Button(frame, text="Clear chat", command=self.clear_chat)
        self.run_generation_button.pack(padx=10, pady=10)

        # Generation Response Field
        self.generation_response_frame = ttk.Frame(self.frame)
        self.generation_response = HtmlFrame(self.generation_response_frame)

        # Loading screen
        self.loading_frame = ttk.Frame(self.frame)
        self.loader = HtmlFrame(self.loading_frame)
        self.load_loading_page()

    def clear_chat(self):
        self.root.messages = []
        self.load_web_page()

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

        self.generation_response_frame.place_forget()
        self.loading_frame.place(y=300, x=0, relwidth=1, height=900)

        if not self.root.messages:
            self.root.messages.append(
                ChatMessage(role="system", content=prompt)
            )

        try:
            thread = threading.Thread(target=question, args=(
                project_name,
                task_requirements,
                prompt,
                max_tokens,
                self.root
            ))

            thread.start()

        except Exception as e:
            messagebox.showerror("Error", "Error occurred while generating response: \n" + str(e))
            self.root.messages = []

    def load_web_page(self):
        tempfile.NamedTemporaryFile(mode='w')
        f = open("temp.html", 'w')
        f.write("<html><body style='background: rgb(28, 28, 28)'>")
        for message in self.root.messages:
            content = message.content.replace("\n", "<br>")
            if message.role == "system":
                continue
            if message.role == "user":
                f.write(f"<p style='color: rgb(255, 255, 255); font-size: 12px; font-family: Arial; margin-right: "
                        f"40px; border-radius: 0 12px 12px 0; background: "
                        f"rgb(117, 92, 129); padding: 10px;'>{content}</p>")
            if message.role == "assistant":
                f.write(f"<p style='color: rgb(255, 255, 255); font-size: 12px; font-family: Arial; margin-left: "
                        f"40px; border-radius: 12px 0 0 12px; background: rgb(117, 92, 129); padding: 10px'>{content}</p>")

        f.write("</body></html>")
        f.flush()
        f.close()
        self.generation_response.load_file(os.path.abspath(f.name), force=True)
        self.generation_response.pack()
        return True

    def load_loading_page(self):
        tempfile.NamedTemporaryFile(mode='r')
        loading_animation = os.path.abspath("assets/loading.png").replace('\\', '/')
        tempfile.NamedTemporaryFile(mode='w')
        f = open("loading.html", 'w')
        f.write(f"<html><body style='background-color: rgb(28, 28, 28)'><img src='file:///{loading_animation}' style"
                f"='width: 300px; height: 300px; margin: auto; display: block; padding-top: 100px'></body></html>")
        f.flush()
        f.close()
        self.loader.load_file(os.path.abspath("loading.html"), force=True)
        self.loader.pack()
        return True
