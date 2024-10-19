import google.generativeai as genai
import mysql.connector

genai.configure(api_key='AIzaSyC_DxC3l3QFjtBbBY65uZBs_xi4cXxIjUU')

chat_commands = {
    "Persona": "You are Raju Bhai, a chatbot designed to chat with a user and send their queries to the SQL bot to access information from a local database about CPUs.",
    "Objective": "You are strictly a messenger. You must pass the user's question to the SQL bot and return the SQL bot's response to the user.",
    "Instructions": "If some one askes your name, you should say 'my name is Raju bhai, Raju bhai unna kannala pathale bang bang bang'. You should pass the user’s question to the SQL bot and send the SQL bot’s response back to the user. Do not answer any questions without consulting the SQL bot.",
    "example": "User: Give me info about 11th gen i5 CPU's. You: 'I will get right to it!' (now send the question to SQL bot)."
}
chat_commands = str(chat_commands)

chat_model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=chat_commands)

sql_commands = {
    "Persona": "You are an AI model that generates SQL queries based on user questions related to CPU benchmarks. Focus on building accurate queries for a database containing CPU benchmark data.",
    "objective": "Generate precise SQL queries based on user questions about CPU performance.",
    "Instructions": "Generate a SQL query that fetches CPU performance details from the 'cpu_performance' table.",
    "example": "Question: What are the specs of Intel i5-12500H? Answer: SELECT * FROM cpu_performance WHERE model = 'i5-12500H';"
}
sql_commands = str(sql_commands)

sql_model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=sql_commands)

def clean_sql_query(query: str):
    cleaned_query = query.replace("```sql", "").replace("```", "").strip()
    return cleaned_query

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
        return f"Database error: {e}"

def process_user_question(question: str):
    try:
        sql_chat = sql_model.start_chat(enable_automatic_function_calling=True)
        sql_query_response = sql_chat.send_message(question)
        sql_query = clean_sql_query(sql_query_response.text.strip())
        db_results = access_database_with_query(sql_query)
        if isinstance(db_results, str):
            return db_results
        elif db_results:
            return db_results
        else:
            return "No data found for the specified CPU."
    except Exception as e:
        return f"An error was encountered: {e}"

def main_chatbot():
    chat_session = chat_model.start_chat(enable_automatic_function_calling=True)

    while True:
        question = input("Enter your question (or type 'stop' to end the convo): ")

        if question.lower() == "stop":
            print("Thank you for chatting with me! Have a great time.")
            break

        sql_response = process_user_question(question)

        if isinstance(sql_response, str):
            chat_response = chat_session.send_message(f"User asked: {question}. SQL bot says: {sql_response}")
        elif sql_response:
            db_results_str = "\n".join([str(row) for row in sql_response])
            chat_response = chat_session.send_message(f"User asked: {question}. Here's what SQL bot found:\n{db_results_str}")

        print(f"Chatbot response: {chat_response.text}")

main_chatbot()
