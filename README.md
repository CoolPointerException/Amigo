# Amigo AI 🔥- software project assistant

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/coolpointerexception)

> Create a detailed description of a Software task, and let the AI prepare the solution.

## Description
This application is designed to assist with software projects. It creates embeddings of your entire
project and provides you with useful information and possible solutions for your Tasks. This reduces the time
spent on searching for solutions and increases the productivity of your team. 
Currently, it supports 3 AI Models: `OpenAI`, `Azure OpenAI` and `Gemini`.

## Architecture

- python 3.11
- llama_index
- tkinter
- Supported AI Models: `OpenAI`, `Azure OpenAI` and `Gemini`

## Setup

### Run executable
Download executable from the latest release and run it. Keep the file in one place, because it will create additional 
files and directories needed for indexing and storing settings.
> The application is not signed, so you will probably get a warning from your OS. If you prefer you can build it on your 
> own. The following instructions require you to use venv. 
> 
> First you need to install requirements: `pip install -r requirements.txt`.
> Then go to `venv/Lib/site-packages/llama_index/__init.py__` and replace reading from VERSION file (lines 3 and 4)
> with a simple assigning of the version number. For example: `__version__ = "0.9.16post1"`.
> Lastly run the command `pyinstaller --onefile main.spec` in the root directory of the project. This will create an executable.

### Run from source
#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Run the application

```bash
python3 main.py
```

## Usage

1. **SETTINGS:** When you are first time using the application, you will need to set all the required settings. Go to Tab Settings
and fill in all the required fields. Settings will be saved to `app_settings.json` file when the application exits and 
will be loaded when you start the application for the second time.

<img src="assets/img.png" alt="settings" height="700"/>

2. **PROJECTS:** Go to tab Projects and click on the button `Select Directory`. Fill in the Project name and optionally the select 
which files should be ignored. Proceed and click on the button `Create Index`. This will create an index of your entire
project. Once it will finish, you will see text 'Done' under the button, and you will be able to select the project 
in the list of projects.

<img src="assets/img_1.png" alt="projects" height="700"/>

3. **TASKS:** Go to tab Tasks and enter your task Description. Then click on the button `Run Generation`. This will 
generate possible solutions for your task.

<img src="assets/img_2.png" alt="tasks" height="700"/>

## Contributing

If you want to contribute see the [Contribution Guide](CONTRIBUTING.md) for more details (you can also find my contact there).
Feedback is also greatly appreciated. If you have some good idea for improvement, don't hesitate to contact me. ❤️

## TODOs

There are a few good to have features that needs to be done:
- integrating with 3rd party project managements tools like: Jira, Asana ...
- [**DONE** ✅] ~~taking advantage of Version Control (git) to create reindexing of a project - only necessary files are reindex~~
- update of GUI - make it more user-friendly and prettier
- [**DONE** ✅] ~~creating a Chat-like interface on Task tab: when you get a response you also have an option to create a reply (to provide additional info ...)~~
- force LLM to return structured response? For example some sort of JSON structure or maybe even something similar as git diff command.

> If we could achieve this, then we could create actions which would automatically modify the files. This would probably require some prompt engineering or fine-tuning of models (currently Models have trouble to determine line numbers)

## Donations

If you like this project, you can buy me a coffee :)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/coolpointerexception)
