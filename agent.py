import os
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_ollama import ChatOllama as Ollama
from langchain_community.agent_toolkits import create_sql_agent

def call_agent():

    load_dotenv()

    llm = Ollama(model="llama3.1", temperature=0, base_url="http://host.docker.internal:11434")
    db = SQLDatabase.from_uri(os.getenv("DB_URL"))
    agent_executor = create_sql_agent(llm, db=db, agent_type="tool-calling",verbose=True)


    agent_executor.invoke({"input": "CRITICAL: You must use the database schema tool to read the tables BEFORE you write any SQL. Do not guess table names. What is the name of the driver who is transporting the Beans, and what type of vehicle are they driving?"})