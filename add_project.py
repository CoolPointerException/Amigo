import os
from time import sleep
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import Gemini, OpenAI, AzureOpenAI
import tkinter as tk


def create_embeddings_openai(
        project_name
):
    # Read txt files from data directory
    documents = SimpleDirectoryReader(project_name).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # save index to disk
    index.set_index_id(project_name)
    index.storage_context.persist("./storage")


def call_openai(gui, client, gpt_deployment_name, message_text, fe_filename):
    try:
        completion = client.chat.completions.create(
            model=gpt_deployment_name,
            messages=message_text,
            temperature=0.7,
            max_tokens=4000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        return completion.choices[0].message.content
    except Exception as e:
        try:
            gui.projects_tab.logs_listbox.insert(tk.END, f"Error processing file: {fe_filename}. Reason: {e}")
            sleep(60)
            completion = client.chat.completions.create(
                model=gpt_deployment_name,
                messages=message_text,
                temperature=0.7,
                max_tokens=4000,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            return completion.choices[0].message.content
        except:
            return None


def add_project(
        gui,
        startpath,
        project_name,
        files_to_skip,
):
    # create a directory with the project name if it does not yet exist
    if not os.path.exists(project_name):
        os.makedirs(project_name)

    for subdir, dirs, files in os.walk(startpath):
        for file in files:
            fe_filename = os.path.join(subdir, file)
            fe_filename = fe_filename.replace("\\", "/")

            # skip if file is an image, or packaged file like zip or anything else
            if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".zip") or file.endswith(".rar") \
                    or file.endswith(".7z") or file.endswith(".tar") or file.endswith(".gz") or file.endswith(".tgz") \
                    or file.endswith(".bz2") or file.endswith(".xz") or file.endswith(".pdf") or file.endswith(".doc") \
                    or file.endswith(".docx") or file.endswith(".ppt") or file.endswith(".pptx") or file.endswith(
                ".xls") or file.endswith(".xlsx") or file.endswith(".ico") or file.endswith(".gif") or \
                    file.endswith(".tif") or fe_filename in files_to_skip:
                gui.projects_tab.logs_listbox.insert(tk.END, "Skipped file: " + fe_filename)
                continue

            gui.projects_tab.logs_listbox.insert(tk.END, "Processing file: " + fe_filename)
            f = open(fe_filename, "r")
            file_contents = f.read()
            f.close()

            text = get_response(gui, file_contents)

            # skip if text is None - Error occurred
            if text is None:
                continue

            # create a file with the same name as the original file, but with the .txt extension in project_name
            # directory. Set the value to the text variable
            fe_filename_cp = fe_filename \
                .replace(startpath + '/', '') \
                .replace("/", "___")
            f = open(project_name + "/" + fe_filename_cp + ".txt", "w")
            f.write(text)
            f.close()

            gui.projects_tab.logs_listbox.insert(tk.END, "Finished processing file: " + fe_filename)

    # create embeddings
    create_embeddings_openai(
        project_name
    )

    # add project to dropdown
    values = list(gui.projects_tab.selected_project["values"])
    gui.projects_tab.selected_project["values"] = values + [f"{project_name} | {startpath}"]

    gui.projects_tab.generating_label.config(text="Done!")


def get_response(gui, file_contents):
    prompt = f"""
        You are an AI assistant that helps people describe what a certain blocks of code does. 
        Try to describe as best as you can what the following code does. CODE:\n\n{file_contents}"""
    return gui.service_context.llm.complete(prompt).text
