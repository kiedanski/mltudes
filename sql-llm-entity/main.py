import os
import openai
from sqlalchemy import text
from llama_index.agent.openai import OpenAIAgent
from typing import List

from llama_index.core.tools import ToolMetadata
from llama_index.core.tools.eval_query_engine import EvalQueryEngineTool, QueryEngineTool
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.tools import FunctionTool
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from sqlalchemy import (
    create_engine,
    MetaData,
)

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]

engine = create_engine(os.environ["DATABASE_URL"])
metadata_obj = MetaData()

llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo") # might need to go to 4

sql_database = SQLDatabase(engine, include_tables=["sales"])

query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["sales"], llm=llm
)

query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="sales_data",
            description=(
                "Provides all the required information about sales on this particular domain"
                "Useful if you need to retrieve any kind of data"
                "This will automatically retrieve data from an SQL database and parse it"
            ),
        ),
    )

def get_unique_values(col_name: str) -> List[str]:
    """

    Given the name of a column in the sales table, it returns all the distinct values
    of that column.

    Parameters:
    col_name (str): The name of the column.

    Returns: The list of all distinct values in the column

    """

    with engine.connect() as con:
        r = con.execute(text(f"SELECT DISTINCT {col_name} from sales")).all()
        return [x[0] for x in r]


unique_values_tool = FunctionTool.from_defaults(fn=get_unique_values)

# query_str = "What is the total amount of sales per city?"
# response = query_engine.query(query_str)
# print(response.metadata["sql_query"])
# print(response.response)


# query_str = "What are the total sales of Naypyitaw? Output only the number"
# response = query_engine.query(query_str)
# print(response.metadata["sql_query"])
# print(response.response)

# query_str = "What was the branch that sold more Electronics?"
# response = query_engine.query(query_str)
# print(response.metadata["sql_query"])
# print(response.response)

# query_str = "How many branches are out there? List them all in alphabetical order. Output should be  a markdown list"
# response = query_engine.query(query_str)
# print(response.metadata["sql_query"])
# print(response.response)





agent = OpenAIAgent.from_tools(
    system_prompt="""
    
    You are an expert data analyst charged with executing SQL queries.
    Some of the SQL queries you receive will be ambiguous and running the exact query will not yield the expected result. 

    In particular, whenever you need to search the table for a particular value, and you are unsure about it, you should check first the existing values in that particular column and check if its there. If it is not (maybe it was misspelled or it is similar), ask the user for clarification.

    If in doubt, always ask the user for clarification.

    """,
    tools=[
        query_engine_tool,
        unique_values_tool
    ],
    llm=llm,
    verbose=True,
)


r = agent.chat("total amount of sales")
print(r)




r = agent.chat("what was the branch that sold more Electronics?")
print(r)

r = agent.chat("electronics is a product line")
