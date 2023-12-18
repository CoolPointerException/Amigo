from llama_index import StorageContext, load_index_from_storage
import tiktoken
from llama_index.llms import ChatMessage

from helpers.add_project import get_response


def question(
    selected_project,
    task,
    is_new_chat,
    max_tokens,
    gui
):
    # parse project name and project directory
    selected_project = selected_project.split(" | ")
    project_name = selected_project[0]
    project_dir = selected_project[1]

    if is_new_chat:
        encoding = tiktoken.get_encoding("cl100k_base")

        # rebuild storage context
        storage_context = StorageContext.from_defaults(persist_dir="./storage")

        # load index
        index = load_index_from_storage(storage_context, project_name)
        retriever = index.as_retriever(similarity_top_k=25)

        # retrieve relevant documents
        nodes = retriever.retrieve(task)

        # add file structure to prompt:
        f = open(project_dir + "/" + project_name + "/project_files_structure.txt", "r")
        system_message = "Project file structure:\n\n" + f.read() + "\n\n"

        # count tokens
        num_tokens = len(encoding.encode(task))
        # if chat is not new, then Project file structure is already inside messages
        if is_new_chat:
            num_tokens += len(encoding.encode(system_message))
        num_tokens += 5000  # add 5000 tokens wiggleroom for responses
        for message in gui.messages:
            num_tokens += len(encoding.encode(str(message)))

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
                system_message += file_name + ":\n'''\n" + file_contents + "\n'''\n"

        # ad task description to messages:
        gui.messages.append(
            ChatMessage(role="system", content=system_message)
        )

    # ad task description to messages:
    gui.messages.append(
        ChatMessage(role="user", content=task)
    )

    response = get_response(gui, gui.messages)

    gui.messages.append(response)

    gui.task_tab.loading_frame.place_forget()
    gui.task_tab.generation_response_frame.place(y=300, x=0, relwidth=1, height=900)
    gui.task_tab.load_web_page()
    return
