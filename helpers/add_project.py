import os
from concurrent.futures import ThreadPoolExecutor
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import ChatMessage
import tkinter as tk
import subprocess


def create_embeddings_openai(
        project_name
):
    # Read txt files from data directory
    documents = SimpleDirectoryReader(project_name).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # save index to disk
    index.set_index_id(project_name)
    index.storage_context.persist("./storage")


def add_git_commit_hash(project_name, gui):
    try:
        sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
        f = open(project_name + "/git_commit_hash.txt", "w")
        f.write(sha)
        f.close()
    except Exception as e:
        gui.projects_tab.logs_listbox.insert(tk.END, f"Could not retrieve git commit hash: {e}")


def git_diff(project_name, gui):
    try:
        current_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
        f = open(project_name + "/git_commit_hash.txt", "r")
        old_commit = f.read()
        f.close()
        diff = subprocess.check_output(['git', 'diff', '--name-only', current_commit, old_commit]).decode('ascii').strip()
        return diff.split("\n")
    except Exception as e:
        gui.projects_tab.logs_listbox.insert(tk.END, f"Could not retrieve git diff: {e}")


def remove_files(project_name, diff, gui):
    try:
        for file in diff:
            file = file.replace("/", "___")
            try:
                os.remove(project_name + "/" + file + ".txt")
                gui.projects_tab.logs_listbox.insert(tk.END, "Removed file: " + file)
            except Exception as e:
                print("Could not remove file: " + str(e))
        os.remove(project_name + "/project_files_structure.txt")
        try:
            os.remove(project_name + "/git_commit_hash.txt")
        except Exception as e:
            print("Could not remove git_commit_hash.txt: " + str(e))
    except Exception as e:
        gui.projects_tab.logs_listbox.insert(tk.END, f"Could not remove files: {e}")


def add_project(
        gui,
        startpath,
        project_name,
        files_to_skip,
        directories,
        is_reindex,
        diff=None,
        threads=1
):
    # create a directory with the project name if it does not yet exist
    if not os.path.exists(project_name):
        os.makedirs(project_name)

    # if reindexing, remove files that were modified or deleted
    if is_reindex:
        remove_files(project_name, diff, gui)

    directories = list(directories)
    skip_generated_txt_files = os.path.join(startpath, project_name).replace("\\", "/")
    directories.append(skip_generated_txt_files)

    # Iterate over files in parallel
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for subdir, dirs, files in os.walk(startpath):
            for file in files:
                executor.submit(generate_summary_for_file, subdir, file, startpath, directories, project_name,
                                files_to_skip, is_reindex, diff, gui)

    # create embeddings
    create_embeddings_openai(
        project_name
    )

    # add project files structure file
    f = open(project_name + "/project_files_structure.txt", "w")
    f.write(list_files(startpath, files_to_skip, directories))
    f.close()

    # add git commit hash if available
    add_git_commit_hash(project_name, gui)

    if not is_reindex:
        # add ignored files to ignored_files.txt
        f = open(project_name + "/ignored_files.txt", "w")
        f.write("\n".join(files_to_skip))
        f.close()

        # add ignored directories to ignored_directories.txt
        f = open(project_name + "/ignored_directories.txt", "w")
        f.write("\n".join(directories))
        f.close()

    # add project to dropdown
    values = list(gui.task_tab.selected_project["values"])
    gui.task_tab.selected_project["values"] = values + [f"{project_name} | {startpath}"]
    gui.projects_tab.reindex_project["values"] = values + [f"{project_name} | {startpath}"]

    gui.projects_tab.generating_label.config(text="Done!")


def generate_summary_for_file(
        subdir,
        file,
        startpath,
        directories,
        project_name,
        files_to_skip,
        is_reindex,
        diff,
        gui
):
    fe_filename = os.path.join(subdir, file)
    fe_filename = fe_filename.replace("\\", "/")

    skip_directory = any(subdir.replace("\\", "/").startswith(s) for s in directories)

    # skip if file is an image, or packaged file like zip or anything else
    if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".zip") or file.endswith(".rar") \
            or file.endswith(".7z") or file.endswith(".tar") or file.endswith(".gz") or file.endswith(".tgz") \
            or file.endswith(".bz2") or file.endswith(".xz") or file.endswith(".pdf") or file.endswith(".doc") \
            or file.endswith(".docx") or file.endswith(".ppt") or file.endswith(".pptx") or file.endswith(
        ".xls") or file.endswith(".xlsx") or file.endswith(".ico") or file.endswith(".gif") or \
            file.endswith(".tif") or fe_filename in files_to_skip or skip_directory:
        gui.projects_tab.logs_listbox.insert(tk.END, "Skipped file: " + fe_filename)
        return

    # if reindexing, skip files that were not modified
    if is_reindex and fe_filename.replace(f"{startpath}/", "") not in diff:
        gui.projects_tab.logs_listbox.insert(tk.END, "Skipped file: " + fe_filename)
        return

    gui.projects_tab.logs_listbox.insert(tk.END, "Processing file: " + fe_filename)
    f = open(fe_filename, "r")
    file_contents = f.read()
    f.close()

    messages = [
        ChatMessage(role="system", content="You are an AI assistant that helps people describe what a certain "
                                           "blocks of code does."),
        ChatMessage(role="user", content=f"Try to describe as best as you can what the following code does. "
                                         f"CODE:\n\n{file_contents}")
    ]

    text = get_response(gui, messages).content

    # skip if text is None - Error occurred
    if text is None:
        return

    # create a file with the same name as the original file, but with the .txt extension in project_name
    # directory. Set the value to the text variable
    fe_filename_cp = fe_filename \
        .replace(startpath + '/', '') \
        .replace("/", "___")
    f = open(project_name + "/" + fe_filename_cp + ".txt", "w")
    f.write(text)
    f.close()

    gui.projects_tab.logs_listbox.insert(tk.END, "Finished processing file: " + fe_filename)


def get_response(gui, messages):
    response = gui.service_context.llm.chat(messages)
    return response.message


def list_files(startpath, skip_files, skip_directories):
    result = ""
    # iterate over all indexed files and directories in order to prepare a project structure file
    for root, dirs, files in os.walk(startpath):
        if any(root.replace("\\", "/").startswith(s) for s in skip_directories):
            continue
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        result += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            if root.replace("\\", "/") + "/" + f in skip_files:
                continue
            result += '{}{}\n'.format(subindent, f)
    return result
