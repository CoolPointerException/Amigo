from tkinter import ttk, scrolledtext, INSERT
import tkinter as tk


class SettingsTab:
    def __init__(self, root, frame):
        self.frame = frame
        self.root = root

        # API Type
        ttk.Label(frame, text="API Type:").grid(column=0, row=0, sticky='W')
        self.api_type = ttk.Combobox(frame, width=88, state="readonly", values=["azure", "openai", "gemini"])
        self.api_type.grid(column=1, row=0, padx=5, pady=5)
        self.api_type.bind('<<ComboboxSelected>>', self.api_type_changed)

        # API Key
        ttk.Label(frame, text="API Key:").grid(column=0, row=1, sticky='W')
        self.api_key_entry = ttk.Entry(frame, width=90)
        self.api_key_entry.grid(column=1, row=1, padx=5, pady=5)

        # API Host URL
        self.api_host_label = ttk.Label(frame, text="API Host URL:")
        self.api_host_label.grid(column=0, row=2, sticky='W')
        self.api_host_entry = ttk.Entry(frame, width=90)
        self.api_host_entry.grid(column=1, row=2, padx=5, pady=5)

        # API Version
        self.api_version_label = ttk.Label(frame, text="API Version:")
        self.api_version_label.grid(column=0, row=3, sticky='W')
        self.api_version_entry = ttk.Entry(frame, width=90)
        self.api_version_entry.grid(column=1, row=3, padx=5, pady=5)

        # GPT Model Name
        ttk.Label(frame, text="GPT Model Name:").grid(column=0, row=4, sticky='W')
        self.gpt_model = ttk.Entry(frame, width=90)
        self.gpt_model.grid(column=1, row=4, padx=5, pady=5)

        # GPT Deployment Name
        self.gpt_deployment_label = ttk.Label(frame, text="GPT Deployment Name:")
        self.gpt_deployment_label.grid(column=0, row=5, sticky='W')
        self.gpt_deployment = ttk.Entry(frame, width=90)
        self.gpt_deployment.grid(column=1, row=5, padx=5, pady=5)

        # Embeddings Model Name
        ttk.Label(frame, text="Embed Model Name:").grid(column=0, row=6, sticky='W')
        self.embeddings_model_entry = ttk.Entry(frame, width=90)
        self.embeddings_model_entry.grid(column=1, row=6, padx=5, pady=5)

        # Embeddings Deployment Name
        self.embeddings_deployment_label = ttk.Label(frame, text="Embed Deployment Name:")
        self.embeddings_deployment_label.grid(column=0, row=7, sticky='W')
        self.embeddings_deployment_entry = ttk.Entry(frame, width=90)
        self.embeddings_deployment_entry.grid(column=1, row=7, padx=5, pady=5)

        # Prompt
        ttk.Label(frame, text="Prompt:").grid(column=0, row=8, sticky='W')
        self.prompt_entry = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=65, height=5)
        self.prompt_entry.configure(state='normal')
        self.prompt_entry.insert(INSERT, """
        You are a programmer who tries to complete tasks that your analytic team provides. 
        They give you a task description and code they think might be relevant. 
        Prepare all the necessary changes that are required for the task to be finished. If the 
        team did not provide enough information, point out what information you still need. 
        If you have enough information then your solutions for tasks should follow these guidelines 
        without any additional explanation:
        \n- include only the code that needs to be modified/added, 
        \n- print line numbers of the code snippet if a file was modified (use the standard with + prefix for 
        added and - for deleted lines) 
        \n-include in the changes also all the required imports 
        \n- follow the coding style and conventions from the existing files 
        \n- do not explain what the code does 
        \n- explain only if there are some things that needs to be checked, before applying changes 
        (vulnerabilities, ambiguity ... ) 
        \n-if you think there are other files that need to be modified, but were not included in the question, 
        point that out (use the project structure as reference) \n-do not create any comments in code snippets
        """)
        self.prompt_entry.grid(column=1, row=8, padx=5, pady=5, rowspan=5)

        # Optional Settings
        ttk.Label(frame, text="Max input token length:").grid(column=0, row=13, sticky='W')
        self.max_tokens = ttk.Entry(frame, width=90)
        self.max_tokens.grid(column=1, row=13, padx=5, pady=5)
        self.max_tokens.insert(INSERT, "64000")
        ttk.Label(frame, text="Number of threads:").grid(column=0, row=14, sticky='W')
        self.threads = ttk.Entry(frame, width=90)
        self.threads.insert(INSERT, "1")
        self.threads.grid(column=1, row=14, padx=5, pady=5)

    def api_type_changed(self, event):
        self.root.isLlamaInitialized = False
        self.show_only_relevant_settings()

    def show_only_relevant_settings(self):
        if self.api_type.get() == "openai":
            self.api_host_label.grid_remove()
            self.api_host_entry.grid_remove()
            self.api_version_label.grid_remove()
            self.api_version_entry.grid_remove()
            self.gpt_deployment_label.grid_remove()
            self.gpt_deployment.grid_remove()
            self.embeddings_deployment_label.grid_remove()
            self.embeddings_deployment_entry.grid_remove()
        if self.api_type.get() == "azure":
            self.api_host_label.grid(column=0, row=2, sticky='W')
            self.api_host_entry.grid(column=1, row=2, padx=5, pady=5)
            self.api_version_label.grid(column=0, row=3, sticky='W')
            self.api_version_entry.grid(column=1, row=3, padx=5, pady=5)
            self.gpt_deployment_label.grid(column=0, row=5, sticky='W')
            self.gpt_deployment.grid(column=1, row=5, padx=5, pady=5)
            self.embeddings_deployment_label.grid(column=0, row=7, sticky='W')
            self.embeddings_deployment_entry.grid(column=1, row=7, padx=5, pady=5)
        if self.api_type.get() == "gemini":
            self.api_version_label.grid_remove()
            self.api_version_entry.grid_remove()
            self.gpt_deployment_label.grid_remove()
            self.gpt_deployment.grid_remove()
            self.embeddings_deployment_label.grid_remove()
            self.embeddings_deployment_entry.grid_remove()
