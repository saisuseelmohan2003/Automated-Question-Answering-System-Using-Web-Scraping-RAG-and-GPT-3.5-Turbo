# 📦 Automated Question Answering System Using Web Scraping, RAG, and GPT-3.5 Turbo

Welcome to the **Automated Question Answering System**! This project uses web scraping to gather product data and combines it with OpenAI's GPT-3.5 Turbo to provide accurate answers to user questions. 

## 🚀 Project Overview

This system automates the process of answering product-related questions stored in a MySQL table. It scrapes relevant data from product web pages and uses the GPT-3.5 Turbo model to generate responses based on the scraped data and the given questions.

## 🌟 Features

- **🔍 Web Scraping**: Collects product data such as title, features, key features, description, and specifications.
- **🧠 Contextual Answer Generation**: Uses the scraped data to provide accurate answers to user questions.
- **💾 Database Integration**: Retrieves questions from and stores answers in a MySQL database.

## ⚙️ Configure MySQL connection:

Update the MySQL connection details in the script:

MYSQL_HOST = 'your_host'
MYSQL_USER = 'your_user'
MYSQL_PASSWORD = 'your_password'
MYSQL_DB = 'your_database'
MYSQL_PORT = your_port

## 🔑 Set up OpenAI API key:

openai.api_key = "your_openai_api_key"


## ▶️ Run the script:

The script will connect to the MySQL database, fetch questions without answers, scrape the required product data, generate answers using GPT-3.5 Turbo, and update the database with the generated answers.

## 🤖 How It Works

💻 Database Connection: The script connects to a MySQL database and fetches questions that need answers.
🌐 Web Scraping: It scrapes product information from specified URLs to gather necessary data.
🧩 Data Aggregation: The scraped data is organized into a structured format.
🔮 Answer Generation: Using the GPT-3.5 Turbo model, the script generates answers to the questions based on the scraped data.
💾 Database Update: The generated answers are updated back into the MySQL database.

## 📝 Function Descriptions

scrape_product_data(url): Scrapes product data from the given URL and returns a dictionary containing the title, features, key features, description, product information, and specifications.

generate_answer(question, product_data): Generates an answer to the given question using the provided product data and the OpenAI API.

process_questions(): Connects to the MySQL database, fetches questions, scrapes product data, generates answers, and updates the database.
