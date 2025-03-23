# **SportsLLM**  
TODO: Add description here

## **Table of Contents**
1. [Introduction](#introduction)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Configuration](#configuration) _(if applicable)_  
6. [Examples](#examples) _(if applicable)_  
7. [API Reference](#api-reference) _(if applicable)_  
8. [Contributing](#contributing)  
9. [Roadmap](#roadmap) _(if applicable)_  
10. [License](#license)  
11. [Acknowledgments](#acknowledgments) _(if applicable)_  

---

## **Introduction**
TODO: Provide a brief introduction to your project, explaining its purpose and what problem it solves.

## **Installation**
### **Prerequisites**
1. **Python 3.8+** - Required for running the custom server
2. **Ollama** - Install from [ollama.com](https://ollama.com/)

### **Setup Instructions**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/SportsLLM.git
   cd SportsLLM
   ```

2. **Install Python Dependencies**
   ```bash
   pip install fastapi uvicorn httpx
   ```

3. **Configure Ollama**
   - Start Ollama on port 11434 (this is the default port)
   ```bash
   ollama serve 
   ```
   - Pull your desired models:
   ```bash
   ollama pull llama3.1
   # Add any other models you want to use
   ```

4. **Start the Custom Server**
   ```bash
   python custom_llm_server.py
   ```
   The server will run on port 11435, acting as a middleware between Open-WebUI and Ollama.

5. **Configure Open-WebUI**
   - Set the Ollama base URL to point to your custom server:
   ```bash
   export OLLAMA_BASE_URL=http://localhost:11435
   ```
   - Start Open-WebUI following their installation instructions

### **Verification**
To verify your installation:
1. Ensure Ollama is running on port 11434
2. Confirm the custom server is running on port 11435
3. Open the Open-WebUI interface
4. You should see your available models in the model selection dropdown
5. Test a chat interaction to ensure everything is working properly

### **Troubleshooting**
- If models aren't showing up, check that Ollama is running and accessible
- If chat isn't working, verify all components are running on their correct ports
- Check the custom server logs for any error messages

## **Usage**
TODO: Add usage instructions

## **Features**
TODO: Add features

## **Contributing**
TODO: Add contributing guidelines

## **License**
TODO: Add license information

## **Examples**
TODO: Add examples

## **API Reference**
TODO: Add API reference

## **Roadmap**
TODO: Add roadmap

## **Acknowledgments**
TODO: Add acknowledgments
