from langchain_core.prompts import ( ChatPromptTemplate, FewShotPromptTemplate, MessagesPlaceholder, PromptTemplate, SystemMessagePromptTemplate, )
from examples import example_selector

system_prefix = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Always give the output.
If the user is customer then don't give the output related to the earnings of any user.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
When generating SQL queries that involve names, ensure to use the LIKE operator for partial matches. Specifically, when a name is referenced, whether it's a user name, company name, or other related entities, use the pattern LIKE '%name%' in the query to capture partial matches. This will include all records that contain the specified name within the relevant fields.
DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database."""
system_suffix = """
    """

few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=PromptTemplate.from_template(
        "User input: {input}\nSQL query: {query}"
    ),
    input_variables=["input", "dialect", "top_k"],
    prefix=system_prefix,
    suffix=system_suffix,
)

full_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
Query: {query}
SQL Result: {result}
Answer:
"""
)

system_suffix_2 = """
"""

def get_system_suffix_2(customer_id):
    return system_suffix_2.format(customer_id=customer_id)

def set_customer_id(customer_id):
    few_shot_prompt_2 =  FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=PromptTemplate.from_template(
            "User input: {input}\nSQL query: {query}"
        ),
        input_variables=["input", "dialect", "top_k"],
        prefix=system_prefix,
        suffix=system_suffix_2.format(customer_id=customer_id),
    )
    return ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate(prompt=few_shot_prompt_2),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
) 
