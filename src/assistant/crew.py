from crewai import Agent, Crew, Task
from crewai.project import CrewBase, agent, crew, task, callback
from .tools.internet_search_tool import InternetSearchTool
from .tools.chart_generation_tool import ChartGenerationTool
from crewai_tools import WebsiteSearchTool, CodeInterpreterTool
import streamlit as st


# Warnings
import warnings
warnings.filterwarnings('ignore')

@CrewBase
class MarketResearchCrew:
    """
    A market research crew for planning, conducting research via web scraping,
    and generating reports.
    """
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    code_interpreter_tool = CodeInterpreterTool(unsafe_mode=True)
    
    @callback
    def callback_function(self, TaskOutput):
        """Callback function to handle agent output."""
        with st.spinner("Processing agent output..."):
            st.write(f"Task: {TaskOutput.agent}")
            st.write(TaskOutput.description)
        

    @agent
    def researcher_agent(self) -> Agent:
        """Agent responsible for conducting web scraping and gathering data."""
        return Agent(
            config=self.agents_config['researcher_agent'],
            verbose=True,
            tools=[InternetSearchTool(), WebsiteSearchTool()],
        )

    # @agent
    # def chart_generation_agent(self) -> Agent:
    #     """Agent responsible for generating charts."""
    #     return Agent(
    #         config=self.agents_config['chart_generation_agent'],
    #         verbose=True,
    #         tools=[ChartGenerationTool()],
    #     )

    # @agent
    # def reporting_agent(self) -> Agent:
    #     """Agent responsible for analyzing data and creating reports."""
    #     return Agent(
    #         config=self.agents_config['reporting_agent'],
    #         verbose=True,
    #     )

    @task
    def research_task(self) -> Task:
        """Task for the researcher agent to gather data using web scraping."""
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher_agent(),
            output='output/market_research_report.md',
            callback=self.callback_function,
        )

    # @task
    # def chart_generation_task(self) -> Task:
    #     """Task for the chart generation agent to create charts."""
    #     return Task(
    #         config=self.tasks_config['chart_generation_task'],
    #         agent=self.chart_generation_agent(),
    #         context=[self.research_task()],
    #         callback=self.callback_function,
    #     )

    # @task
    # def reporting_task(self) -> Task:
    #     """Task for the reporting analyst to create the market research report."""
    #     return Task(
    #         config=self.tasks_config['reporting_task'],
    #         agent=self.reporting_agent(),
    #         context=[self.research_task(), self.chart_generation_task()],
    #         output_file='output/market_research_report.md',
    #         callback=self.callback_function,
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Market Research Crew with defined agents and tasks."""
        return Crew(
            # agents=[self.researcher_agent(), self.chart_generation_agent(), self.reporting_agent()],
            # tasks=[self.research_task(), self.chart_generation_task(), self.reporting_task()],
            agents=[self.researcher_agent()],
            tasks=[self.research_task()],
            verbose=True,
        )
