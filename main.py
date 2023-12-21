import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
import sv_ttk

from gui.tab_projects import ProjectsTab
from gui.settings import load_settings, save_settings
from gui.tab_settings import SettingsTab
from gui.tab_task import TaskTab


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Amigo")
        self.geometry("900x1100")
        self.style = Style()
        self.isLlamaInitialized = False
        sv_ttk.set_theme("dark")
        self.messages = []

        self.style.configure('W.TButton', font=('calibri', 18, 'bold', 'underline'), borderwidth='4')
        self.style.configure('W.Label', font=('calibri', 13, 'bold'))

        # Create the tab control
        self.tab_control = ttk.Notebook(self)

        # Create tabs
        self.settings_frame = ttk.Frame(self.tab_control)
        self.task_frame = ttk.Frame(self.tab_control)
        self.projects_frame = ttk.Frame(self.tab_control)

        # Add tabs to notebook
        self.tab_control.add(self.task_frame, text='Task')
        self.tab_control.add(self.projects_frame, text='Projects')
        self.tab_control.add(self.settings_frame, text='Settings')

        # Init UI
        self.settings_tab = SettingsTab(self, self.settings_frame)
        self.task_tab = TaskTab(self, self.task_frame)
        self.projects_tab = ProjectsTab(self, self.projects_frame)

        # Init settings
        self.settings_file = 'app_settings.json'
        load_settings(self)

        self.tab_control.pack(expand=1, fill="both")

    def on_close(self):
        save_settings(self)
        self.destroy()

    def main(self):
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.mainloop()


if __name__ == "__main__":
    app = Application()
    app.main()
