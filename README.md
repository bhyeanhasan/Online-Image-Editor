### Online Image Ediotor

##### Visit The Live Website [Click Here](https://bhyeanhasan.pythonanywhere.com/)

## Prerequisites

- Python 3.8 or higher installed on your system.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bhyeanhasan/Online-Image-Editor.git
    cd Online-Image-Editor
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    -   **Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Apply migrations (if this is the first run):**
    ```bash
    python manage.py migrate
    ```

2.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

3.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.
