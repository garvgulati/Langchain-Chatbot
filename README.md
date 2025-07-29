# Langchain-Chatbot
A basic chatbot that leverages the power of a modern language model and the convenience of a development framework.

This project is an advanced chatbot built using Python, showcasing a powerful combination of modern AI technologies. It provides a highly interactive and functional user experience.

## ✨ Key Features

-   **Interactive Web UI**: A clean and user-friendly web interface powered by Streamlit.
-   **Real-time Streaming**: Responses from the AI are streamed token-by-token for a dynamic, "live" feel.
-   **High-Speed Performance**: Leverages the Gemma model via the Groq API for incredibly fast inference speeds.
-   **Customizable Persona**: Easily define the chatbot's personality and behavior through a system prompt in the UI.
-   **Conversation Memory**: Remembers the context of the conversation for more coherent and relevant interactions.
-   **Model Selection**: Allows choosing from several popular models available on the Groq platform.

## 🛠️ Setup and Installation

### Prerequisites

-   Python 3.8 or newer
-   `pip` and `venv` (usually included with Python)

### Step-by-Step Instructions

1.  **Download the Project Files:**
    Save the `app.py` and `requirements.txt` files into a new project folder.

2.  **Install Dependencies:**
    With your virtual environment active, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Get Your Groq API Key:**

4.  **Run the Application:**
    Execute the following command in your terminal:
    ```bash
    streamlit run app.py
    ```
    This will start the web server and open the application in your default browser.

## 🚀 How to Use

1.  **Open the App:** The app should open automatically at `http://localhost:8501`.
2.  **Enter API Key:** In the sidebar on the left, paste your Groq API key.
3.  **Configure Persona (Optional):** You can edit the system prompt in the sidebar to change how the chatbot behaves.
4.  **Start Chatting:** Type your message in the input box at the bottom of the screen and press Enter. Enjoy the fast, streaming responses!
