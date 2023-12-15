import os

from llama_index import StorageContext, load_index_from_storage
import tiktoken
from llama_index.llms import Gemini

import markdown

from add_project import get_response


def list_files(startpath):
    result = ""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        result += '{}{}/\n'.format(indent, os.path.basename(root))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            result += '{}{}\n'.format(subindent, f)
    return result


def question(
    selected_project,
    task,
    prompt,
    max_tokens,
    gui
):
    # parse project name and project directory
    selected_project = selected_project.split(" | ")
    project_name = selected_project[0]
    project_dir = selected_project[1]

    encoding = tiktoken.get_encoding("cl100k_base")

    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir="storage")

    # load index
    index = load_index_from_storage(storage_context, project_name)
    retriever = index.as_retriever(similarity_top_k=25)

    # retrieve relevant documents
    nodes = retriever.retrieve(task)

    # ad task description to prompt:
    prompt += "\n\nTask description:\n\n" + task + "\n\n"
    # add file structure to prompt:
    prompt += "\n\nProject file structure:\n\n" + list_files(project_dir) + "\n\n"
    num_tokens = len(encoding.encode(prompt))

    # iterate over documents that were the best matches
    for node in nodes:
        file_name = node.metadata['file_name'][:-4].replace("___", "/")
        file_path = project_dir + "/" + file_name
        # open file and read contents
        with open(file_path, 'r') as file:
            file_contents = file.read()
            tokens = len(encoding.encode(file_contents))

            # stop adding files to context if max_tokens is reached
            if num_tokens + tokens > int(max_tokens):
                break

            num_tokens += tokens
            prompt += file_name + ":\n'''\n" + file_contents + "\n'''\n"

    response = get_response(gui, prompt)

    return response


