import tkinter as tk
from tkinter import INSERT
import json


def load_settings(self):
    try:
        with open(self.settings_file, 'r') as f:
            settings = json.load(f)
            if settings.get('api_version'):
                self.settings_tab.api_version_entry.delete(0, tk.END)
                self.settings_tab.api_version_entry.insert(0, settings.get('api_version'))
            if settings.get('api_type'):
                self.settings_tab.api_type.set(settings.get('api_type'))
                self.settings_tab.show_only_relevant_settings()
            if settings.get('api_key'):
                self.settings_tab.api_key_entry.delete(0, tk.END)
                self.settings_tab.api_key_entry.insert(0, settings.get('api_key'))
            if settings.get('api_host'):
                self.settings_tab.api_host_entry.delete(0, tk.END)
                self.settings_tab.api_host_entry.insert(0, settings.get('api_host'))
            if settings.get('gpt_model'):
                self.settings_tab.gpt_model.delete(0, tk.END)
                self.settings_tab.gpt_model.insert(0, settings.get('gpt_model'))
            if settings.get('gpt_deployment'):
                self.settings_tab.gpt_deployment.delete(0, tk.END)
                self.settings_tab.gpt_deployment.insert(0, settings.get('gpt_deployment'))
            if settings.get('embeddings_model'):
                self.settings_tab.embeddings_model_entry.delete(0, tk.END)
                self.settings_tab.embeddings_model_entry.insert(0, settings.get('embeddings_model'))
            if settings.get('embeddings_deployment'):
                self.settings_tab.embeddings_deployment_entry.delete(0, tk.END)
                self.settings_tab.embeddings_deployment_entry.insert(0, settings.get('embeddings_deployment'))
            if settings.get('prompt'):
                self.settings_tab.prompt_entry.delete('1.0', tk.END)
                self.settings_tab.prompt_entry.insert(INSERT, settings.get('prompt', 'This is a prompt'))
            if settings.get('projects'):
                projects = settings.get('projects')
                for project in projects:
                    values = list(self.task_tab.selected_project["values"])
                    self.task_tab.selected_project["values"] = values + [project]
                    self.projects_tab.reindex_project["values"] = values + [project]
            if settings.get('selected_project'):
                self.task_tab.selected_project.set(settings.get('selected_project'))
                self.projects_tab.reindex_project.set(settings.get('selected_project'))
            if settings.get('max_tokens'):
                self.settings_tab.max_tokens.delete(0, tk.END)
                self.settings_tab.max_tokens.insert(INSERT, settings.get('max_tokens'))
            if settings.get('threads'):
                self.settings_tab.threads.delete(0, tk.END)
                self.settings_tab.threads.insert(INSERT, settings.get('threads'))

    except FileNotFoundError:
        print("Settings file not found. Using default values.")


def save_settings(self):
    settings = {
        'api_version': self.settings_tab.api_version_entry.get(),
        'api_type': self.settings_tab.api_type.get(),
        'api_key': self.settings_tab.api_key_entry.get(),
        'api_host': self.settings_tab.api_host_entry.get(),
        'gpt_model': self.settings_tab.gpt_model.get(),
        'gpt_deployment': self.settings_tab.gpt_deployment.get(),
        'embeddings_model': self.settings_tab.embeddings_model_entry.get(),
        'embeddings_deployment': self.settings_tab.embeddings_deployment_entry.get(),
        'prompt': self.settings_tab.prompt_entry.get("1.0", tk.END).strip(),
        'projects': list(self.task_tab.selected_project["values"]),
        'selected_project': self.task_tab.selected_project.get(),
        'max_tokens': self.settings_tab.max_tokens.get(),
        'threads': self.settings_tab.threads.get()
    }
    with open(self.settings_file, 'w') as f:
        json.dump(settings, f, indent=4)
