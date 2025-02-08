from duckduckgo_search import DDGS
from crewai.tools import BaseTool


class InternetSearchTool(BaseTool):
    name: str = "Internet Search Tool"
    description: str = (
        "Search the Internet for relevant information based on a query."
    )

    def _run(self, query: str, max_results: int = 5, region: str = 'wt-wt', safesearch: str = 'moderate'):
        """
        Perform a DuckDuckGo search and return results.
        
        Args:
            query (str): The search query.
            max_results (int): Maximum number of results to retrieve.
            region (str): Region for the search (default is 'wt-wt' for worldwide).
            safesearch (str): Safe search mode ('off', 'moderate', 'strict').

        Returns:
            list: A list of dictionaries containing search results.
        """
        try:
            ddgs = DDGS()
            results = ddgs.text(keywords=query, region=region, safesearch=safesearch, max_results=max_results)
            formatted_results = [
                {
                    "title": result.get("title", "No Title"),
                    "url": result.get("href", ""),
                    "snippet": result.get("body", "No Description")
                }
                for result in results
            ]
            return formatted_results
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    def search_and_print(self, query: str, max_results: int = 100):
        """
        Helper function to print results for debugging or demo purposes.
        """
        results = self._run(query, max_results=max_results)
        for idx, result in enumerate(results, start=1):
            print(f"Result {idx}:")
            print(f"Title: {result['title']}")
            print(f"URL: {result['url']}")
            print(f"Snippet: {result['snippet']}\n")

