import os
from crewai import Agent, Task, Crew, Process as P
from duckduckgo_search import DDGS
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from datetime import datetime

def timestamp():
    # return year month
    return f"Year: {datetime.now().year}, Month: {datetime.now().month}"

def step_callback(step):
    print(f"Step {step} completed.")

@tool("Internet Search Tool")
def internet_search_tool(query: str) -> list:
    """Search the Internet for relevant information based on a query."""
    ddgs = DDGS()
    results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
    print(f"Search results for '{query}':")
    for result in results:
        print(result['title'])
        print(result['href'])
    return results

def create_agent(role, goal, backstory, tools=None, allow_delegation=False, llm_model="gpt-4o-mini"):
    """Create a generalized agent with specific role and goals."""
    return Agent(
        role=role,
        goal=goal,
        verbose=True,
        backstory=backstory,
        tools=tools or [],
        allow_delegation=allow_delegation,
        llm=ChatOpenAI(model=llm_model, streaming=True),
    )

def create_task(description, expected_output, agent=None):
    """Create a generalized task with a description and expected output."""
    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
    )

def create_crew(agents, tasks, manager_role, manager_goal, process_type=P.hierarchical):
    """Create and manage a crew with specified agents, tasks, and a manager."""
    manager_agent = create_agent(
        role=manager_role,
        goal=manager_goal,
        backstory="An experienced project manager guiding the team to success.",
        allow_delegation=True,
    )
    crew = Crew(
        agents=agents,
        tasks=tasks,
        manager_agent=manager_agent,
        process=process_type,
        verbose=True,
    )
    return crew

# Example user inputs for creating agents and tasks
user_input = {
    "researcher_role": "Researcher",
    "researcher_goal": f"Conduct research on technology trends for {timestamp()}",
    "researcher_backstory": "An expert researcher with a deep understanding of various fields.",
    "writer_role": "Writer",
    "writer_goal": "Compose engaging articles based on research findings",
    "writer_backstory": "A talented writer who translates complex ideas into compelling narratives.",
    "manager_role": "Project Manager",
    "manager_goal": "Ensure efficient task completion and team coordination.",
    "research_task_description": "Investigate the latest trends in technology.",
    "research_task_output": "A detailed report in bullet points.",
    "writing_task_description": "Write an article based on the research findings.",
    "writing_task_output": "A well-structured article suitable for publication.",
}

# Create agents based on user input
researcher = create_agent(
    role=user_input["researcher_role"],
    goal=user_input["researcher_goal"],
    backstory=user_input["researcher_backstory"],
    tools=[internet_search_tool]
)

writer = create_agent(
    role=user_input["writer_role"],
    goal=user_input["writer_goal"],
    backstory=user_input["writer_backstory"]
)

# Define tasks based on user input
research_task = create_task(
    description=user_input["research_task_description"],
    expected_output=user_input["research_task_output"],
    agent=researcher,
)

writing_task = create_task(
    description=user_input["writing_task_description"],
    expected_output=user_input["writing_task_output"],
    agent=writer,
)

# Create the crew with agents and tasks
crew = create_crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    manager_role=user_input["manager_role"],
    manager_goal=user_input["manager_goal"],
    process_type=P.hierarchical
)

# Kick off the process with dynamic input
result = crew.kickoff(inputs={'topic': 'Current technology trends'})
print(result)
