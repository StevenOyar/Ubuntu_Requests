# Ubuntu_Requests
 ubuntu Image Fetcher
====================

A simple yet powerful Python script for mindfully and respectfully downloading images from the web.

This tool is built on the philosophy of **Ubuntu**, a concept from Southern Africa that translates to "I am because we are." It is designed to be a responsible member of the internet community by preventing duplicate downloads, validating content, and being considerate of server load.

### Features

*   **Duplicate Detection**: Uses file hashing to automatically detect and skip images you've already downloaded, saving you time and storage.
    
*   **Content Validation**: Performs safety checks to ensure the downloaded file is a safe image format (e.g., .jpg, .png) and not a potentially malicious file.
    
*   **Polite Requests**: Includes a respectful User-Agent and adds a small delay when fetching multiple images to avoid overwhelming web servers.
    
*   **Robust Error Handling**: Provides clear, helpful messages for common issues like timeouts, connection errors, and permission failures.
    
*   **Intuitive Interface**: A simple command-line menu guides you through the process of fetching single or multiple images.
    

### Prerequisites

To run this script, you need to have:

*   Python 3.x installed
    
*   The requests library
    

You can install the requests library using pip:

`  pip install requests   `

### How to Use

1.  **Save the file**: Save the provided code into a file named ubuntu\_image\_fetcher.py.
    
2.  python ubuntu\_image\_fetcher.py
    
3.  **Choose an option**: Follow the on-screen prompts to either fetch a single image URL or a list of multiple URLs.
    

The script will automatically create a directory named Fetched\_Images in the same folder where you run it. All successfully downloaded images will be saved there.

### Community & Philosophy

This project is a small tribute to the Ubuntu philosophy. We believe that by building tools that are respectful and considerate, we can help create a more harmonious digital community for everyone. Feel free to use, modify, and share this tool.