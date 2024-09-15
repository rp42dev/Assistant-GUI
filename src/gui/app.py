import streamlit as st
from assistant.crew import AssistantCrew
# get current year 
from datetime import datetime
year = datetime
year = year.now().year

task_options = {
    "research_task": "Research Task",
    "reporting_task": "Reporting Task"
}

class AppUI:
    
    def generate_report(self, topic, description, year):
        inputs = {
            "topic": topic,
            "description": description,
            "year": year
        }
        output = AssistantCrew().crew().kickoff(inputs=inputs)
        return output.raw
        
    def sidebar(self):
        with st.sidebar:
            st.title("Research Assistant")
            st.write("Enter the topic and details of the research")
           
            topic = st.text_input("Topic", key="topic", placeholder="Enter the topic")
            description = st.text_area("Details", key="details", placeholder="Enter the details")
            
            if st.button("Start Research"):
                st.session_state["generating"] = True
            # if st.session_state["report"] and st.session_state["report"] != "":
            #     st.selectbox("Select the report", options=["report.md"], key="report")
                
    def render(self):
        st.set_page_config(page_title="Research Assistant", page_icon="🔍")
        if "topic" not in st.session_state:
            st.session_state["topic"] = ""
        if "details" not in st.session_state:
            st.session_state["details"] = ""
        if "report" not in st.session_state:
            st.session_state["report"] = "hello world"
        if "generating" not in st.session_state:
            st.session_state["generating"] = False
            
        self.sidebar()
        if st.session_state["generating"]:
            st.session_state["report"] = ""
            with st.chat_message("AI"):
                st.session_state["report"] = self.generate_report(
                    st.session_state["topic"],
                    st.session_state["details"],
                    year
                )
                st.write(st.session_state["report"], unsafe_allow_html=True)
            st.session_state["generating"] = False

if __name__ == "__main__":
    AppUI().render()