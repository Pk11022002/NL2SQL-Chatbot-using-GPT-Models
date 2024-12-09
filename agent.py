import os 
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import AzureChatOpenAI
from prompts import full_prompt
from langchain_core.output_parsers import StrOutputParser
from main import db

# Initialize the LLM using AzureChatOpenAI
llm = AzureChatOpenAI(
    base_url=os.getenv("AOAI_GPT4o_BASE_URL"),
    openai_api_version=os.getenv("AOAI_GPT4o_VERSION"),
    openai_api_key=os.getenv("AOAI_GPT4o_KEY"),
    openai_api_type="azure",
    model=os.getenv("AOAI_GPT4o_MODEL"),
    temperature=0
)

# Create the SQL agent
agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=False,
    agent_executor_kwargs={'return_intermediate_steps': True},
    top_k=1000,
    agent_type="openai-tools",
)
def get_agent_2(prompt):
    return create_sql_agent(
        llm=llm,
        db=db,
        prompt=prompt,
        verbose=False,
        agent_executor_kwargs={'return_intermediate_steps': True},
        top_k=100000,
        agent_type="openai-tools",
    )



# agent.invoke(
#     {
#         "input": "Base earning of nazre in july 2024"
#     }
# )


