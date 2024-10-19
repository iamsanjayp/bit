import google.generativeai as genai

genai.configure(api_key='AIzaSyC_DxC3l3QFjtBbBY65uZBs_xi4cXxIjUU')

commands = {"Persona":"You are a chat bot designed to answer questions asked by computer enthusiasts. You should have a very upbeat and sarcasting tone.",
            "objective":"The enthusiasts will ask questions about computers. The main objective is to resolv as many of their doubts and issues precisely and quickly.",
            "Instructions":"You can tell the customer about yourself if they ask for it.The customers question should only be about computers. Do not deviate from this topic. You should only answer questions about computers. Be sure to not repeat the answers that you have already provided.",
            "Goal":"Most apt anwser for the question asked by the enthusiast",
            "example":"Question-Hey lina!, what is the cpu benchmark specs of intel-12500H?. Answer-Ofcourse here are the benchmarks for i5-12500H,  generation = 12th, series = H, model = i5-12500H, base_clock = 2.50, boost_clock = 4.50, cores = 6, threads = 12, cinebench_score = 1500, geekbench_score = 5200, release_date = 2021-01-01",
            "remember":"remember the above commands."}
commands=str(commands)
import mysql.connector
def access_database_for_cpu_benchmarks(model: str):
    connection = mysql.connector.connect(
        host="localhost",
        database="cpu_benchmarks",
        user="root",
        password="climax"
    )
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM cpu_performance"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows[0] if rows else None

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=commands,tools=[access_database_for_cpu_benchmarks])

chat = model.start_chat(enable_automatic_function_calling=True)

while True:
    question = input("Enter your question (or type stop to end the convo): ")

    if question.lower() == "stop":
        print("Thank you for chatting with me! Have a great time.")
        break
    try:
        print(f"Sending question: {question}")  # Debugging line
          # Extract the CPU name from the question
        response = chat.send_message(question)
        print(response.text)
    except Exception as e:
        print(f"An exception occurred while processing the question '{question}': {e}. Please try again.")

