from tkinter import messagebox
from llama_index import ServiceContext, set_global_service_context, OpenAIEmbedding
from llama_index.embeddings import AzureOpenAIEmbedding, GeminiEmbedding
from llama_index.llms import Gemini, OpenAI, AzureOpenAI

from gui.input_validator import validate, Properties


def init_llama_index(self, api_type):
    if self.isLlamaInitialized:
        return

    llm = None
    embed_model = None

    if api_type == "azure":
        is_valid = validate(self, [
            Properties.API_BASE,
            Properties.API_VERSION,
            Properties.API_KEY,
            Properties.GPT_MODEL,
            Properties.GPT_DEPLOYMENT,
            Properties.EMBEDDING_MODEL,
            Properties.EMBEDDING_DEPLOYMENT,
        ])
        if not is_valid:
            return

        api_base = self.settings_tab.api_host_entry.get()
        api_version = self.settings_tab.api_version_entry.get()
        api_key = self.settings_tab.api_key_entry.get()
        gpt_model_name = self.settings_tab.gpt_model.get()
        gpt_deployment_name = self.settings_tab.gpt_deployment.get()
        embedding_model_name = self.settings_tab.embeddings_model_entry.get()
        embedding_deployment_name = self.settings_tab.embeddings_deployment_entry.get()

        llm = AzureOpenAI(
            deployment_name=gpt_deployment_name,
            model=gpt_model_name,
            api_key=api_key,
            azure_endpoint=api_base,
            api_version=api_version
        )

        embed_model = AzureOpenAIEmbedding(
            model=embedding_model_name,
            deployment_name=embedding_deployment_name,
            api_key=api_key,
            azure_endpoint=api_base,
            api_version=api_version,
        )

    if api_type == "openai":
        is_valid = validate(self, [
            Properties.API_KEY,
            Properties.GPT_MODEL,
            Properties.EMBEDDING_MODEL,
        ])
        if not is_valid:
            return

        api_key = self.settings_tab.api_key_entry.get()
        gpt_model_name = self.settings_tab.gpt_model.get()
        embedding_model_name = self.settings_tab.embeddings_model_entry.get()

        llm = OpenAI(
            model=gpt_model_name,
            api_key=api_key
        )
        embed_model = OpenAIEmbedding(
            model=embedding_model_name,
            api_key=api_key,
        )

    if api_type == "gemini":
        is_valid = validate(self, [
            Properties.API_KEY,
            Properties.GPT_MODEL,
            Properties.EMBEDDING_MODEL,
        ])
        if not is_valid:
            return

        api_key = self.settings_tab.api_key_entry.get()
        gpt_model_name = self.settings_tab.gpt_model.get()
        embedding_model_name = self.settings_tab.embeddings_model_entry.get()

        llm = Gemini(
            model_name=gpt_model_name,
            api_key=api_key
        )
        embed_model = GeminiEmbedding(
            model_name=embedding_model_name,
            api_key=api_key,
        )

    if not llm or not embed_model:
        messagebox.showerror("Error", "Error occurred while initializing llama_index.")
        return

    self.service_context = ServiceContext.from_defaults(
        llm=llm,
        embed_model=embed_model,
    )

    set_global_service_context(self.service_context)
    self.isLlamaInitialized = True
