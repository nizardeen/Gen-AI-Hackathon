# Medimate

## Introduction

**Medimate** is an intelligent companion designed to provide **personalized medicine guidance**. It helps healthcare professionals and patients determine whether a specific tablet or medication is suitable based on the **patient's medical history**.  

The system considers various patient attributes such as chronic conditions, allergies, genetic disorders, and previous treatments to provide **tailored recommendations**. By leveraging AI and large language models, Medimate not only validates the suitability of a medication but also provides insights about potential adverse reactions, and expected recovery times. This makes it a **reliable support tool for informed medical decisions** in a personalized healthcare setting.

## 🎥 Demo Video

[Watch Demo](demo/demo.webm)

---

## Project Components

1. **Database**  
   - PostgreSQL stores patient records and medication history.  
   - The database is set up inside **Docker** for easy deployment and reproducibility.  

2. **MCP Server**  
   - Orchestrates tool calls and manages interactions between the app and the LLM model.  

3. **LLM Model**  
   - `meta-llama/llama-3.3-70b-instruct` using **Cerebras**.  
   - Connected via **OpenRouter** for API-based model queries.  

4. **User Interface**  
   - **Streamlit** front-end allows inputting patient details and receiving recommendations.  

---

## Getting Started

### Prerequisites

   - Python (3.10+)
   - Serper API key
   - Cerebras API key
   - Openrouter API key

### Setup
1. Clone the repository:
    ```bash
    git clone git@github.com:nizardeen/Gen-AI-Hackathon.git
    ```

2. Install Required Dependencies:
   Create a `virtualenv` and activate it to install the below dependencies
   ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory:
    ```
    SERPER_API_KEY=<Your_serper_key>
    CEREBRAS_API_KEY=<Your_cerebras_key>
    OPEN_ROUTER_KEY=<Your_openrouter_key>
    DB_CONNECTION_STR=<DB_connection_string>
    ```

## Usage

### Building and Running

1. Build Docker for Databse:
    ```bash
    docker compose up --build
    ```
    Ensure `start.sh` creates the database, tables, and imports any initial CSV data.

2. Run the MCP server (Run in separate terminal):
    ```bash
    python3 main.py
    ```
    The server will listen on port 8000 and accept MCP requests at `/sse` endpoint

3. Launch the Streamlit app:
    ```bash
    streamlit run streamlit_app.py
    ```

4. Open the UI in your browser: `http://localhost:8501`

## Features

  - Personalized medication recommendations
  - Automatic validation of patient metrics (chronic conditions, genetic disorders, drug allergies and current medication)
  - AI-driven insights for safe consumption of tablet, and adverse reactions
  - Intuitive Streamlit interface


## Acknowledgements
  - [Model Context Protocol] (https://github.com/modelcontextprotocol/python-sdk)
  - [Serper API] (https://serper.dev/)
  - [Cerebras] (https://www.cerebras.ai/)
  - [Openrouter] (https://openrouter.ai/)