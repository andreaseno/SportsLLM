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
TODO: Provide a brief introduction to the project, explaining its purpose and what problem it solves.

## **Installation**
### **Prerequisites**
Install Ollama at https://ollama.com/
Install NodeJS at https://nodejs.org/en

### **Setup**

Below are the steps needed to run the app for the first time. These steps will only work if you have the correct prerequisite installations. 

1. Clone the repo into your local environment using `git clone https://github.com/andreaseno/SportsLLM.git`

2. Enter into the frontend application using `cd SportsLLM/open-webui`

3. Install the node depencies using `npm install`

4. Move into the backend using `cd backend`

5. Install python dependencies using `pip install -r requirements.txt  -U`

6. Build the webapp using `npm run build`

7. Pull the desired model to run with using `ollama pull llama3.1:latest` (replace llama3.1:latest with whatever model you want. I recommend 3.2:latest if you want a smaller model that runs faster)

8. Make sure Ollama server is running by running `ollama serve` in a separate terminal

9. Run the webapp using `./start.sh`


### **Running the App**

To run the app, you should already have ollama started as detailed in step 7 of the setup. Every time you make a change to a .svelte file, you need to rerun step 6 to get changes to show (this does not apply to changes to .py files). Step 8 must be ran every time the app needs to be started, and needs to be reran to show ANY new changes. 
