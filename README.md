# Overview
An interactive modular ChatBot assistant capable of handling a wide variety of user requests by branching tasks to specialized chains. The chains, built using Branching Chain architecture of LangChain process specific intents execute the required functions, and return the corresponding response to the user. Built with Flask and Python, the assistant has native access to the Windows APIs and integrates several features like system control, multimedia handling, and more.


## Architecture

### 1. **Input Handling**

- User provides input through the chatbot interface.
- Input is processed via a Flask API and sent to the central **`chat_service.py`** for classification.

### 2. **Intent Recognition**

- Intent recognition is performed using:
  - A Language Model
  - Rule-based fallback logic for straightforward tasks.
- Identified intent determines the chain to execute.

### 3. **Branching**

- The input is routed to the appropriate chain based on the intent which includes system management controls using appropriate Windows APIs or nomral chat branch chain.
- Check [Features](#features) for all the available branches that is currently available in the assistant, or are going to be available soon.  <br>
<i> <b> Note - The branches are not final and are subjected to future changes. </b> </i>

### 4. **Chain Execution**

- Each chain contains modularized service functions to process the task.
- Functions interact with APIs, system commands, or databases as needed through thee corresponding services in `app/services`

### 5. **Response Construction**

- The chain returns the task result or an error message to the central service.
- The chatbot constructs a user-friendly response and sends it back to the user.

---

## Features
1. **System Control Chain**

   - Turn on/off WiFi, Bluetooth, or adjust system volume.

2. **Multimedia Control Chain**

   - Control media playback (play, pause, volume adjustments, etc.).

3. **Chatbot Interaction Chain**

   - Answer general queries, tell jokes, or engage in small talk.

4. **File Management Chain**

   - Search for files, create folders, or manage documents.

5. **Calendar and Scheduling Chain**

   - Add events, check schedules, and set reminders.

6. **Coding Chain**

   - Generate and explain code, suggest libraries, refactor, translate code, as well as provide a comprehensive how-to guide for creating the project.

7. **Semantic Search Chain**

   - Retrieve relevant information from documents or knowledge bases.

8. **Task Automation Chain**

   - Automate repetitive processes like batch file renaming, create tasks in Task Schedular similar to creation of cron jobs, define and perform a function after every time duration specified.

9. **Internet Related Chain**

   - Search for resources on the internet, summarize the searched resources (in pdfs, docx, xlsx, etc), perform other information retrieval operations with proper citations, write/compose/read/draft emails, fetch news with fact appropriate fact checking and near zero bias.

10. **Developer Tools Chain**

    - Assist with developer-related tasks like debugging or running scripts, and finding and terminating errors in a code.
<br>
---

## WorkFlow
[![](https://mermaid.ink/img/pako:eNqNlMFunDAQhl9l5NNWSl5gD5XaXUXtYdVW7KlxhSZ4AlawjYxJRFb77h3Aa7J0VcHF-J9_vhlg8EkUTpHYitJjU8FxLy3wpW3ThbwN_lGKLHhtS9h8H7RPUvyB-_vPUGCg0nn9TrlhQs3Gw7DCZpcikFIm6jJnBDXoW8pjqJ_qwc9B9LAZV4jEfiZdJ40cRYG80ZblCrU9SfHVoy0q2OwvEdgNEaacpZ04iyQGATfQt4EM7JwN3tVSjPh2FCfb49IzgVN3N6mHrg7akNK4IJsUSPR_vWsqsCU8ucBvnYNYBO1sLFFMkcS_4VxT4EHXBAe0WJIhGyL8mdXclGbGL3yresearEIPaBVkRUWqq3nqLv3H6PwAt-2rKjn1wTnhR2mGXzn-x8rIoA26gIzQF9VlVKI6D8u1bQ35iO0LfOmCM_jhOwZWE3VhWUP9hl69oSf41ZHvI7SKYgJfu9Zw9_RKtWv4jz06V7cRrOg1D8M-kRe-NegfoSIfgelUEnfCsBW14pPrNGRLwT5DUmz5lgfjRQppz-xDfkFZbwuxDb6jO-FdV1Zi-4x1y7uuUXyG7DXy8WeS2qD97dxlf_4LVPXCbQ?type=png)](https://mermaid.live/edit#pako:eNqNlMFunDAQhl9l5NNWSl5gD5XaXUXtYdVW7KlxhSZ4AlawjYxJRFb77h3Aa7J0VcHF-J9_vhlg8EkUTpHYitJjU8FxLy3wpW3ThbwN_lGKLHhtS9h8H7RPUvyB-_vPUGCg0nn9TrlhQs3Gw7DCZpcikFIm6jJnBDXoW8pjqJ_qwc9B9LAZV4jEfiZdJ40cRYG80ZblCrU9SfHVoy0q2OwvEdgNEaacpZ04iyQGATfQt4EM7JwN3tVSjPh2FCfb49IzgVN3N6mHrg7akNK4IJsUSPR_vWsqsCU8ucBvnYNYBO1sLFFMkcS_4VxT4EHXBAe0WJIhGyL8mdXclGbGL3yresearEIPaBVkRUWqq3nqLv3H6PwAt-2rKjn1wTnhR2mGXzn-x8rIoA26gIzQF9VlVKI6D8u1bQ35iO0LfOmCM_jhOwZWE3VhWUP9hl69oSf41ZHvI7SKYgJfu9Zw9_RKtWv4jz06V7cRrOg1D8M-kRe-NegfoSIfgelUEnfCsBW14pPrNGRLwT5DUmz5lgfjRQppz-xDfkFZbwuxDb6jO-FdV1Zi-4x1y7uuUXyG7DXy8WeS2qD97dxlf_4LVPXCbQ)

**<u>Input Received</u>**: The user message is sent to the Flask chatbot endpoint. <br>
**<u>Intent Recognition</u>**: Intent identified as **`list_wifi_networks()`**. <br>
**<u>Branch to System Control Chain</u>**: Task routed to the System Control Chain. <br>
**<u>Execute Function</u>**: **`WifiService.list_wifi_networks()`** is called. <br>
**<u>Response</u>**: Success message returned: `"WiFi has been turned on."`

## Windows API integration
To reduce the dependency on third party packages and to achieve a greater level of system integration, system components have been written using the Win32 API which is then compiled into a DLL and then called using Python's `ctypes` library. The source code of all the functions are avaiilable in `app/services/libraries/source` directory. To compile the code into corresponding library, Microsoft's C++ Compiler (cl.exe) is used -
```shell
cl /LD bluetooth.cpp /link Bthprops.lib /Fe:bluetooth.dll
```
This takes the bluetooth.cpp file as input, links it to Bthprops library and then generates a bluetooth.dll file that can be then be imported and used.

### Note - The system currently only supports -
- GPT4All Open Source Models: Models have to be exported to .gguf file in `app/models` directory
- Groq AI: Just enter the Groq API Key in .env file and it will default to ChatGroq
- Preliminary support for OpenAI and Anthropic coming in the next commit!