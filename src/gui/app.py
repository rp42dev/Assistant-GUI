import streamlit as st
from pathlib import Path
from assistant.crew import MarketResearchCrew
from datetime import datetime

def read_markdown_file(file_path):
    """Reads a Markdown file and converts it to HTML."""
    if Path(file_path).exists():
        return Path(file_path).read_text()
    return ""

# Get the current year
current_year = datetime.now().year
class AppUI:
    def __init__(self):
        self.task_options = {
            "research_task": "Research Task",
            "reporting_task": "Reporting Task"
        }

    def render_report(self):
        """Renders the generated report UI."""
        st.title("Generated Report")
        st.write(read_markdown_file("output/market_research_report.md"), unsafe_allow_html=True)

    def generate_report(self, topic, industry, description, location, year):
        """Generates a market research report."""
        crew = MarketResearchCrew()
        inputs = {"topic": topic, "industry": industry, "description": description, "location": location, "year": year}
        
        output = crew.crew().kickoff(inputs=inputs)

        # Simulated report generation
        report_content = read_markdown_file("output/market_research_report.md")
        if report_content:
            st.session_state["report"] = report_content
        else:
            st.error("No report content found. Ensure the research process completes successfully.")

    def sidebar(self):
        """Sidebar for user input."""
        with st.sidebar:
            st.title("Research Assistant")
            st.write("Enter research details:")

            st.session_state["topic"] = st.text_input("Topic", st.session_state.get("topic", ""), placeholder="Enter the topic")
            st.session_state["industry"] = st.text_input("Industry", st.session_state.get("industry", ""), placeholder="Enter the industry")
            st.session_state["description"] = st.text_area("Description", st.session_state.get("description", ""), placeholder="Enter the description")
            st.session_state["location"] = st.text_input("Location", st.session_state.get("location", ""), placeholder="Global, Country, or City")

            if st.button("Start Research"):
                st.session_state["generating"] = True
                self.generate_report(st.session_state["topic"], st.session_state["industry"], st.session_state["description"], st.session_state["location"], current_year)

    def render(self):
        """Renders the main UI."""
        st.set_page_config(page_title="Research Assistant", page_icon="🔍", layout="wide")

        # Initialize session state variables
        st.session_state.setdefault("report", "")
        st.session_state.setdefault("generating", False)

        # Sidebar for inputs
        self.sidebar()

        # Main UI
        st.title("AI-Powered Market Research Assistant")
        st.write("Generate detailed market research reports.")

        if st.session_state["generating"]:
            st.info("Generating the report...")

        if st.session_state["report"]:
            st.subheader("Generated Report")
            self.render_report()


if __name__ == "__main__":
    AppUI().render()


