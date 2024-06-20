import mysql.connector
import requests
from bs4 import BeautifulSoup
import openai

# Project name
PROJECT_NAME = "Automated Question Answering System Using Web Scraping, RAG and GPT-3.5 Turbo"
print(f"{PROJECT_NAME}\n")
print("Welcome to the Automated Question Answering System!")

# MySQL connection details
MYSQL_HOST = ''
MYSQL_USER = ''
MYSQL_PASSWORD = ''
MYSQL_DB = ''
MYSQL_PORT = 

# OpenAI API key
openai.api_key = ""

# Web scraping function
def scrape_product_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title_elem = soup.find('div', {'class': 'product-header-name jm-mb-xs jm-body-m-bold', 'id': 'pdp_product_name'})

        features_elems = soup.select('ul.product-key-features-list li.product-key-features-list-item')
        features = [feature.text.strip() for feature in features_elems] if features_elems else ["Features not found"]

        key_features_elem = soup.find('section', {'class': 'product-key-features'})
        if key_features_elem:
            key_features_list = key_features_elem.find('ul', {'class': 'product-key-features-list'})
            if key_features_list:
                key_features_elems = key_features_list.find_all('li')
                key_features = [feature.text.strip() for feature in key_features_elems]
            else:
                key_features = ["Key Features not found"]
        else:
            key_features = ["Key Features section not found"]

        specifications = {}
        specifications_section = soup.find('section', {'class': 'product-specifications'})
        if specifications_section:
            tables = specifications_section.find_all('table', {'class': 'product-specifications-table'})
            for table in tables:
                rows = table.find_all('tr', {'class': 'product-specifications-table-item'})
                for row in rows:
                    header = row.find('th', {'class': 'product-specifications-table-item-header'})
                    data = row.find('td', {'class': 'product-specifications-table-item-data'})
                    if header and data:
                        specifications[header.text.strip()] = data.text.strip()

        description_elem = soup.find('div', {'id': 'pdp_description'})
        product_info_elem = soup.find('div', {'id': 'pdp_product_information'})

        title = title_elem.text.strip() if title_elem else "Title not found"
        description = description_elem.text.strip() if description_elem else "Description not found"
        product_info = product_info_elem.text.strip() if product_info_elem else "Product Information not found"

        return {
            'Title': title,
            'Features': features,
            'Key Features': key_features,
            'Description': description,
            'Product Information': product_info,
            'Specifications': specifications
        }
    except Exception as e:
        print(f"Error scraping URL {url}: {e}")
        return None

# Function to generate answer using OpenAI API with RAG
def generate_answer(question, product_data):
    context = f"""
    Title: {product_data['Title']}
    Features: {', '.join(product_data['Features'])}
    Key Features: {', '.join(product_data['Key Features'])}
    Description: {product_data['Description']}
    Product Information: {product_data['Product Information']}
    Specifications: {product_data['Specifications']}
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who provides accurate answers based on the provided context. Answer only the relevant questions. If the user asks an irrelevant question, respond with 'out of context' or 'I can't answer'."},
                {"role": "system", "content": context},
                {"role": "user", "content": question}
            ],
            max_tokens=150
        )
        answer = response.choices[0].message['content'].strip()
        if "out of context" in answer.lower() or "i can't answer" in answer.lower():
            return "I can't answer"
        return answer
    except Exception as e:
        print(f"Error generating answer for question '{question}': {e}")
        return None

# Connect to the database and process records
def process_questions():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            port=MYSQL_PORT
        )
        print("Connected successfully")
        cursor = conn.cursor(dictionary=True)

        # Fetch records with NULL answers
        cursor.execute("SELECT * FROM questions_table WHERE answers IS NULL")
        rows = cursor.fetchall()

        for row in rows:
            url = row['urls']
            question = row['questions']
            product_type = row['product_type']
            
            print(f"Processing question: {question}")

            # Scrape data from the URL
            product_data = scrape_product_data(url)
            if not product_data:
                continue  # Skip if scraping failed

            # Generate answer based on the question and scraped data
            answer = generate_answer(question, product_data)
            if not answer:
                continue  # Skip if answer generation failed

            # Update the answer in the database
            try:
                update_query = "UPDATE questions_table SET answers = %s WHERE urls = %s AND questions = %s"
                cursor.execute(update_query, (answer, url, question))
                conn.commit()
                print("Answer column is updated")
            except Exception as e:
                print(f"Error updating answer for question '{question}': {e}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Error processing questions: {e}")

# Execute the process
if __name__ == "__main__":
    process_questions()
