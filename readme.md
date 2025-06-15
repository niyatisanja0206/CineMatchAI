# 🎬 Bollywood Movie Recommendation System

An AI-powered web app that recommends Bollywood movies based on your preferences and fetches detailed movie info using Wikipedia and DuckDuckGo. Built with **Streamlit**, **LangChain**, and **Azure GPT-4o**.


## 🚀 Features

- 🔥 Get Bollywood movie recommendations based on:
  - Genre
  - Actor / Actress
  - Director
  - Year Range
- 📚 Movie details from **Wikipedia**
- 🌐 Relevant links from **DuckDuckGo**
- 🧠 GPT-4o via Azure OpenAI
- 🔐 Environment variable support via `.env`


## 🧰 Tech Stack

- Streamlit
- LangChain
- Azure GPT-4o (via Azure OpenAI)
- DuckDuckGo Search
- Wikipedia API
- Python 3.8+


## 🛠️ Setup Instructions

### Clone the Repository

git clone https://github.com/your-username/bollywood-recommender.git
cd bollywood-recommender

### Create a Virtual Environment

python -m venv venv

### Activate:
**Windows:**
venv\Scripts\activate

**Mac/Linux:**
source venv/bin/activate

### Install Requirements
pip install -r requirements.txt

###  Create a .env File
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_API_BASE=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_API_VERSION=2024-05-01-preview

### Run the App
streamlit run app.py


## Future Enhancements

 Add movie poster integration (OMDb/TMDb)

 Deploy on Streamlit Cloud

 Better fallback handling for missing data

