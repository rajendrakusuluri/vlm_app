# VLM Web Application Instructions

This document provides instructions for setting up and running the VLM Web Application, consisting of a FastAPI backend and a Streamlit frontend.

## Prerequisites

*   Python 3.10+
*   pip

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repository_url>
    cd vlm_app
    ```

2.  **Create a virtual environment and install dependencies:**

    We'll do this separately for the backend and frontend.  A virtual environment helps isolate project dependencies.

    *   **Backend:**
        ```bash
        cd backend
        python -m venv venv  # Create the virtual environment
        source venv/bin/activate  # On Linux/macOS; activate the environment
        # venv\Scripts\activate  # On Windows; activate the environment
        pip install -r requirements.txt  # Install dependencies
        cd ..  # Go back to the project root
        ```

    *   **Frontend:**
        ```bash
        cd frontend
        python -m venv venv  # Create the virtual environment
        source venv/bin/activate  # On Linux/macOS; activate the environment
        # venv\Scripts\activate  # On Windows; activate the environment
        pip install -r requirements.txt  # Install dependencies
        cd ..  # Go back to the project root
        ```
## Configuration

*   **VLM Integration:** Implement the VLM interaction within `backend/vlm_interface.py`.  Refer to the example interface provided in the complete documentation for details on expected inputs and outputs.

*   **Environment Variables:** Store sensitive information (e.g., VLM API keys) in environment variables using a `.env` file in the project root. Use `python-dotenv` to load these variables.  Remember to add `.env` to your `.gitignore`.

*   **Backend URL:** Ensure the `BACKEND_URL` variable in `frontend/app.py` points to the correct address and port of your FastAPI backend.

## Usage

1.  **Start the Backend:**

    ```bash
    cd backend
    source venv/bin/activate  # Activate the virtual environment again if needed
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

2.  **Start the Frontend:**

    ```bash
    cd frontend
    source venv/bin/activate  # Activate the virtual environment again if needed
    streamlit run app.py --server.port 8501
    ```

3.  **Access the Application:**

    Open your web browser and go to the address shown in the Streamlit terminal (usually `http://localhost:8501`).

## Important Notes

*   Expand upon the basic error handling provided in the code.

*   **CORS:** Configure the `allow_origins` setting in `backend/main.py` for production to only allow requests from your frontend's domain. **Avoid using `"*"` due to security risks.**

*   Consider containerizing your application using Docker for easier deployment.

*   Access the automatically generated OpenAPI/Swagger documentation at `http://localhost:8000/docs` after starting the backend.

*   See the complete project documentation for detailed explanations of dependencies and configuration options.