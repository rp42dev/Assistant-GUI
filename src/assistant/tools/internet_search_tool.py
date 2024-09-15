from duckduckgo_search import DDGS
from crewai_tools import BaseTool


class InternetSearchTool(BaseTool):
    name: str = "Internet Search Tool"
    description: str = (
        "Search the Internet for relevant information based on a query."
    )
    def _run(self, query: str):
        ddgs = DDGS()
        results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=5)
        print(f"Search results for '{query}':")
        for result in results:
            print(result['title'])
            print(result['href'])
        return results
