import os
from dotenv import load_dotenv
from langchain_aws import ChatBedrock
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent

load_dotenv()

llm = ChatBedrock(
    model_id="meta.llama3-8b-instruct-v1:0",
    model_kwargs={"temperature": 0},
    region_name=os.getenv("AWS_REGION", "us-east-1") # Let Boto3 handle the routing!
)

db = SQLDatabase.from_uri(os.getenv("DB_URL"))

def lambda_handler(event, context):
    try:

        body = {}
        if event.get("body"):
            body = json.loads(event["body"])

        user_input = body.get(
            "input",
            "CRITICAL: You must use the database schema tool to read the tables BEFORE you write any SQL. Do not guess table names. What is the name of the driver who is transporting the Beans, and what type of vehicle are they driving?"
        )
        
        agent_executor = create_sql_agent(
            llm,
            db=db,
            agent_type="tool-calling",
            verbose=True
        )

        result = agent_executor.invoke({"input": user_input})

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "result": result
            })
        }

    except Exception as e:

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": str(e)
            })
        }