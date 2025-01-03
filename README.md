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
- Functions interact with APIs, system commands, or databases as needed through thee corresponding services in `src/backend/app/services`

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

   - Generate and explain code, suggest libraries, refactor, translate code, as well as provide a comprehensive how-to f

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
[![](https://mermaid.ink/img/pako:eNqNlFFr2zAQgP_KoacU2j-Qh0GXMDZY2IYDg1XD3KyrLWpJRpZbvJD_vrOtyIubB-fF8d13312UQydROEViK0qPTQXHvbTAH22bLuRt8E9SZMFrW8LmyxC7k-I3PDx8gAIDlc7rv5QbNtQMHoYnbHYpA6lksi5rRlGDvqU8pvqpH3wfgh424xOisZ9N10WjR1Egb7TlcIXanqT46NEWFWz2lwzshgxbztJOnkURi4AH6NtABnbOBu9qKUZ9OwYn7GnJTOI03U3roauDNqQ0LswmJZL9PbumAyPhjwt86pzEImhnY4tiyiT_DXJNg0-6JjigxZIM2RDlzxzNTWlm_YJbNTvWZBV6QKsgKypSXc1bd5k_ZucfcBtf0-knYahoqvzqeIXmY3qbUqnLLXRNi4wM2qALyAh9UV02KEbnHbrG1piP2L7AYxec-X_uwNFkXSBrrJ_Rqzf0BD868n2UVjGYxNfUGu-eXql2DZ_g0bm6jWJFr3kY3pN5wa1Rfxv-mChMl5W4F4ZR1IovtNNQLQVzhqTY8lfelxcppD0zh3xAWW8LsQ2-o3vhXVdWYvuMdctvXaP4atlr5FvRXJAG7S_nTITO_wB4_srr?type=png)](https://mermaid.live/edit#pako:eNqNlFFr2zAQgP_KoacU2j-Qh0GXMDZY2IYDg1XD3KyrLWpJRpZbvJD_vrOtyIubB-fF8d13312UQydROEViK0qPTQXHvbTAH22bLuRt8E9SZMFrW8LmyxC7k-I3PDx8gAIDlc7rv5QbNtQMHoYnbHYpA6lksi5rRlGDvqU8pvqpH3wfgh424xOisZ9N10WjR1Egb7TlcIXanqT46NEWFWz2lwzshgxbztJOnkURi4AH6NtABnbOBu9qKUZ9OwYn7GnJTOI03U3roauDNqQ0LswmJZL9PbumAyPhjwt86pzEImhnY4tiyiT_DXJNg0-6JjigxZIM2RDlzxzNTWlm_YJbNTvWZBV6QKsgKypSXc1bd5k_ZucfcBtf0-knYahoqvzqeIXmY3qbUqnLLXRNi4wM2qALyAh9UV02KEbnHbrG1piP2L7AYxec-X_uwNFkXSBrrJ_Rqzf0BD868n2UVjGYxNfUGu-eXql2DZ_g0bm6jWJFr3kY3pN5wa1Rfxv-mChMl5W4F4ZR1IovtNNQLQVzhqTY8lfelxcppD0zh3xAWW8LsQ2-o3vhXVdWYvuMdctvXaP4atlr5FvRXJAG7S_nTITO_wB4_srr)

**<u>Input Received</u>**: The user message is sent to the Flask chatbot endpoint. <br>
**<u>Intent Recognition</u>**: Intent identified as **`turn_on_wifi`**. <br>
**<u>Branch to System Control Chain</u>**: Task routed to the System Control Chain. <br>
**<u>Execute Function</u>**: **`wifi_service.turn_on_wifi()`** is called. <br>
**<u>Response</u>**: Success message returned: `"WiFi has been turned on."`

