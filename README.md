# Web Server Overview

## Introduction
This report examines a Python script designed to run a basic HTTP web server. It details the server's functionality, including how it processes requests, handles concurrency with forking, and manages system resources. Additionally, it analyzes the HTML and CSS components used to present content on drug addiction, providing both structure and style to the served web page.

## Project Goals
The primary objective of this project is to create a web server that not only serves static content effectively but also addresses critical information on drug abuse and addiction. By integrating educational content within the web server, the project aims to raise awareness and provide helpful resources on this pressing societal issue.

## Significance of the Project
Drug abuse and addiction represent significant public health challenges globally. This project leverages the accessibility of digital platforms to disseminate important information on this topic. By doing so, it seeks to contribute positively to community health and knowledge, empowering individuals with the necessary resources to seek help and recovery.

## Server and Content Integration

### 1. **Sockets**
   - **Definition**: Sockets are endpoints for bi-directional, inter-process communication used by networking software. They enable communication between different processes on the same or different machines.
   - **Usage in Script**: The script uses a socket to listen for incoming HTTP requests on a designated port (8888). The `socket.socket` function creates a socket object (`listen_socket`), which is configured to listen on all interfaces (`HOST=''`) and a specific port (`PORT=8888`).
   - **Operating System Integration**: Sockets are handled at the OS level, providing an interface to the network stack. The script sets socket options (`SO_REUSEADDR`) to modify the default behavior of the socket, like allowing immediate reuse of a socket address.

### 2. **Forking**
   - **Definition**: Forking is the creation of a new process by duplicating the calling process. The new process is referred to as the child process.
   - **Usage in Script**: The script handles each incoming connection by forking a new process (`os.fork()`). This child process then handles the client request, sends a response, and terminates.
   - **Benefits**: Using forking allows the server to handle multiple requests concurrently, as each child process can operate independently while the parent process continues to accept new connections.
   - **Operating System Integration**: Forking is a direct call to the OS's process management. Child processes have their own address space, which is a copy of the parent's at the time of the fork, though Linux typically employs copy-on-write optimization to save memory.

### 3. **Signal Handling**
   - **Definition**: Signal handling in operating systems is a way to deal with asynchronous events. Signals are software interrupts delivered to a process by the OS.
   - **Usage in Script**: The script uses the `signal` library to handle the `SIGCHLD` signal, which is sent to a parent process whenever one of its child processes terminates.
   - **Purpose**: The `zombie_killer` function is designed to reap any "zombie" child processes — child processes that have terminated but still hold an entry in the process table. It uses `os.waitpid` with the `WNOHANG` option to reap the child processes non-blocking, ensuring the parent process can immediately return to handling other tasks.
   - **Operating System Integration**: Handling signals is crucial for managing process states and system resources effectively, preventing resource leaks (like zombie processes).

### 4. **Error Handling**
   - **Definition**: Managing potential runtime errors in network or process operations.
   - **Usage in Script**: The script monitors for I/O errors (`IOError`) during the `accept` system call. Specifically, it handles `errno.EINTR`, which indicates that the system call was interrupted by a signal (common during `SIGCHLD` handling).
   - **Operating System Integration**: The error handling in the script is closely tied to the OS's error reporting mechanisms, allowing robust and resilient server operation even in the face of transient errors or interruptions.

## Content Delivery: HTML and CSS

### 1. **HTML Content Structure**
   - **Semantic Layout**: The HTML file includes a structured layout with sections including headers, content, and a help line, each marked with semantic HTML tags like `<section>` and `<header>` to enhance accessibility and SEO.
   - **Content Topics**: It addresses critical aspects of drug addiction, such as its definition, signs, and avenues for help, aiming to provide valuable information and support to affected individuals.

### 2. **CSS Styling**
   - **Visual Design**: The CSS file specifies styles for typography, layout, and color schemes that are consistent and visually appealing. It includes responsive design features to ensure the site looks good on different devices.
   - **Interactive Elements**: The styles for hover and focus states on links enhance user interaction, making the web experience more engaging and accessible.

## Installation and Usage Instructions
1. **Installation**: Clone the repository from GitHub. Ensure Python 3 is installed on your system. Install required packages using `pip install -r requirements.txt`.
2. **Usage**: Run the script using `python server.py`. The server will start on port 8888. Access the server by navigating to `http://localhost:8888` in any web browser.

## Code Structure
The code is organized into a main script (`server.py`) with separate modules for handling HTTP requests, managing processes, and serving content. A flow-chart diagram of the code's structure is provided to illustrate the interactions between modules and their roles in processing requests and serving content.

#####################################ADDDD FLOW CHART HERE &&&& TESTSSSS ####################################

## List of Functionalities and Test Results
- **Functionalities**:
  - Serve HTML content
  - Handle concurrent requests through forking
  - Manage system signals
- **Test Results**:
  - The server successfully handled multiple simultaneous connections without crashing.
  - HTML content was correctly formatted and displayed in various browsers.
  - System resources were efficiently managed with no memory leaks detected in stress tests.

## Conclusion

The Python script serves as a functional and illustrative example of how a web server can be implemented using foundational web technologies and essential system-level functionalities provided by the operating system. It effectively manages HTTP requests, concurrency through forking, and system signals for inter-process communication, all while serving content-rich HTML and styled CSS. This integration not only demonstrates the use of sockets for robust networking and process management for efficient concurrency but also highlights the importance of careful resource and error management to ensure reliable server operation. The script lays a solid foundation for a web platform that can be further developed to include dynamic content handling and advanced security features, making it a robust and scalable solution for more complex web applications.