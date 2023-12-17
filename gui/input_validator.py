from tkinter import messagebox
import tkinter as tk
from enum import Enum


forbidden_names = ["storage", "venv", ".git", ".idea", "__pycache__", "inspectionProfiles"]


class Properties(Enum):
    PROJECT_NAME = 1
    SELECTED_DIRECTORY = 2
    API_TYPE = 3
    API_BASE = 4
    API_VERSION = 5
    API_KEY = 6
    GPT_MODEL = 7
    GPT_DEPLOYMENT = 8
    EMBEDDING_MODEL = 9
    EMBEDDING_DEPLOYMENT = 10
    PROMPT = 11
    MAX_TOKENS = 12
    TASK_REQUIREMENTS = 13
    SELECTED_PROJECT = 14


def validate(gui, properties):
    for prop in properties:
        match prop:
            case Properties.PROJECT_NAME:
                project_name = gui.projects_tab.project_name_entry.get()
                if not project_name:
                    messagebox.showerror("Error", "Please enter a project name.")
                    return False

                if project_name in forbidden_names:
                    messagebox.showerror("Error", "Please enter a valid project name. \nForbidden names:\n - " + "\n - "
                                         .join(forbidden_names))
                    return False
            case Properties.SELECTED_DIRECTORY:
                selected_directory = gui.projects_tab.selected_directory
                if not selected_directory:
                    messagebox.showerror("Error", "Please select a directory.")
                    return False
            case Properties.API_TYPE:
                api_type = gui.settings_tab.api_type.get()
                if not api_type:
                    messagebox.showerror("Error", "Please select API type in Settings Tab.")
                    return False
            case Properties.API_BASE:
                api_base = gui.settings_tab.api_host_entry.get()
                if not api_base:
                    messagebox.showerror("Error", "Please enter API base in Settings Tab.")
                    return False
            case Properties.API_VERSION:
                api_version = gui.settings_tab.api_version_entry.get()
                if not api_version:
                    messagebox.showerror("Error", "Please enter API version in Settings Tab.")
                    return False
            case Properties.API_KEY:
                api_key = gui.settings_tab.api_key_entry.get()
                if not api_key:
                    messagebox.showerror("Error", "Please enter API key in Settings Tab.")
                    return False
            case Properties.GPT_MODEL:
                gpt_model = gui.settings_tab.gpt_model.get()
                if not gpt_model:
                    messagebox.showerror("Error", "Please enter GPT model name in Settings Tab.")
                    return False
            case Properties.GPT_DEPLOYMENT:
                gpt_deployment = gui.settings_tab.gpt_deployment.get()
                if not gpt_deployment:
                    messagebox.showerror("Error", "Please enter GPT deployment name in Settings Tab.")
                    return False
            case Properties.EMBEDDING_MODEL:
                embedding_model = gui.settings_tab.embeddings_model_entry.get()
                if not embedding_model:
                    messagebox.showerror("Error", "Please enter embedding model name in Settings Tab.")
                    return False
            case Properties.EMBEDDING_DEPLOYMENT:
                embedding_deployment = gui.settings_tab.embeddings_deployment_entry.get()
                if not embedding_deployment:
                    messagebox.showerror("Error", "Please enter embedding deployment name in Settings Tab.")
                    return False
            case Properties.PROMPT:
                prompt = gui.settings_tab.prompt_entry.get("1.0", tk.END)
                if not prompt:
                    messagebox.showerror("Error", "Please enter a prompt in Settings Tab.")
                    return False
            case Properties.MAX_TOKENS:
                max_tokens = gui.settings_tab.max_tokens.get()
                if not max_tokens:
                    messagebox.showerror("Error", "Please enter max tokens in Settings Tab.")
                    return False
            case Properties.TASK_REQUIREMENTS:
                task_requirements = gui.task_tab.task_requirements_entry.get("1.0", tk.END)
                if not task_requirements:
                    messagebox.showerror("Error", "Please enter a Task requirements.")
                    return False
            case Properties.SELECTED_PROJECT:
                selected_project = gui.projects_tab.selected_project.get()
                if not selected_project:
                    messagebox.showerror("Error", "Please select a project.")
                    return False
    return True


def is_api_type_set(gui):
    api_key = gui.settings_tab.api_type.get()
    if not api_key:
        messagebox.showerror("Error", "Please enter API key in Settings Tab.")
        return False
    return True
