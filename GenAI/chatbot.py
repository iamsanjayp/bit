import google.generativeai as genai
import mysql.connector

# Configure the AI model for SQL query generation
genai.configure(api_key='AIzaSyC_DxC3l3QFjtBbBY65uZBs_xi4cXxIjUU')

# SQL query generation AI model
sql_commands = {
    "Persona": "You are an AI model that generates SQL queries based on user questions related to CPU benchmarks. Focus on building accurate queries for a database containing CPU benchmark data.",
    "objective": "Generate precise SQL queries based on user questions about CPU performance.",
    "Instructions": "Generate a SQL query that fetches CPU performance details from the 'cpu_performance' table based on the input provided. The table contains data on 11th, 12th, and 13th-gen processors.",
    "example": "Question: What are the specs of Intel i5-12500H? Answer: SELECT * FROM cpu_performance WHERE model = 'i5-12500H';"
}
sql_commands = str(sql_commands)

sql_model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=sql_commands)

# Function to clean SQL query
def clean_sql_query(query: str):
    # Remove any markdown or extra formatting added by the model
    cleaned_query = query.replace("```sql", "").replace("```", "").strip()
    return cleaned_query

# Function to access database for CPU benchmarks
def access_database_with_query(query: str):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="cpu_benchmarks",
            user="root",
            password="climax"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows if rows else None
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        return None

# Function to handle the user question and SQL query logic
def process_user_question(question: str):
    try:
        # Use second model to generate SQL query based on the user's question
        sql_chat = sql_model.start_chat(enable_automatic_function_calling=True)
        sql_query_response = sql_chat.send_message(question)
        sql_query = clean_sql_query(sql_query_response.text.strip())

        print(f"Generated SQL query: {sql_query}")

        # Access the database using the cleaned SQL query
        db_results = access_database_with_query(sql_query)
        if db_results:
            for row in db_results:
                print(f"CPU Data: {row}")
        else:
            print("No data found for the specified CPU.")
    
    except Exception as e:
        print(f"An exception occurred: {e}")

# Main loop to interact with the user
while True:
    question = input("Enter your question (or type 'stop' to end the convo): ")

    if question.lower() == "stop":
        print("Thank you for chatting with me! Have a great time.")
        break

    process_user_question(question)
