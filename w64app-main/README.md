# Python Project Setup Guide

## Install Python

Make sure Python 3 is installed on your machine.

## Setup (Run only once)

1. Create a virtual environment for your project:
    ```bash
    python3 -m venv **project-name**
    ```

2. Create a `.env` file at the root of the project directory.  
   Copy the items from the `.env.example` into your `.env` file and update the values accordingly.

## To Run the Project

1. Activate the virtual environment:
    ```bash
    source **project-name**/bin/activate
    ```

2. Install the required dependencies:
    ```bash
    pip3 install -r requirements.txt
    ```

## Running Files

You can run the project files as follows:

- For Python scripts (example):
    ```bash
    python3 src/main.py
    ```

- Or, use Jupyter Notebook inside /src to run notebooks:
    ```bash
    Jupiter notebook
    ```

That's it! You are all set to start working on the project.
