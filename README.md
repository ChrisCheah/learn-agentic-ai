# Learn Agentic AI

This repository contains demonstrations and applications for learning about agentic AI systems. It includes a contextual chatbot built with LangChain and a Flask web application for selecting AI "roles" or personas.

## Project Structure

```
.
├── app.py                  # Flask web application for role selection
├── manus_demo2.ipynb       # Jupyter notebook demonstrating a contextual chatbot
├── requirements.txt        # Python dependencies
├── templates/              # HTML templates for the Flask app
│   ├── base.html
│   ├── index.html
│   └── role_detail.html
└── README.md               # This documentation file
```

## 1. Environment Setup

Follow these steps to set up your local environment.

### Prerequisites

- Python 3.9+
- A tool to run Jupyter notebooks (like VS Code with the Jupyter extension or a standalone Jupyter installation).

### a. Environment Variables

This project uses an `.env` file to manage secret keys, such as your OpenAI API key.

1.  Ensure you have a file named `.env` in the root of the project directory.
2.  Add your OpenAI API key to the file like this:

    ```
    OPENAI_API_KEY="sk-..."
    ```

### b. Install Dependencies

All required Python libraries are listed in the `requirements.txt` file. For a full setup, it is recommended to install from this file.

1.  It is recommended to create and activate a virtual environment first:
    ```sh
    # Create a virtual environment
    python -m venv .venv

    # Activate it (Windows)
    .\.venv\Scripts\activate
    ```
    *Note: On macOS/Linux, the activation command is `source .venv/bin/activate`.*

2.  Install all libraries using pip and the `requirements.txt` file (recommended):
    ```sh
    pip install -r requirements.txt
    ```
    
    Alternatively, to run just the Flask application, you can install Flask directly:
    ```sh
    pip install Flask
    ```

## 2. Running the Applications

### a. Flask Role Selector App

The Flask app provides a web interface to browse different AI roles.

1.  Run the `app.py` script from your terminal:
    ```sh
    python app.py
    ```

2.  Open your web browser and go to the following address:
    [http://127.0.0.1:5001](http://127.0.0.1:5001)

### b. Contextual Chatbot Notebook

The `manus_demo2.ipynb` notebook demonstrates how to build a chatbot that remembers conversation history.

1.  Start your Jupyter Notebook server or open the file in a compatible IDE like VS Code.
2.  Open `manus_demo2.ipynb`.
3.  Run the cells in the notebook sequentially to see the chatbot in action. The notebook will demonstrate how conversation sessions can be maintained independently.