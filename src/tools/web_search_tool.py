from langchain_core.tools import InjectedToolArg, tool
from typing import Annotated
import uuid
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

BRAVE_SEARCH_API_URL = "https://api.search.brave.com/res/v1/web/search"


class WebSearchTool:  
    def __init__(self, tool_id:str=str(uuid.uuid4()), tool_name:str="websearch_tool"):
        self.tool_id = tool_id
        self.tool_name = tool_name

    @staticmethod
    def brave_search_fn(
        query: str,
        count: Annotated[int, InjectedToolArg] = 3
    ) -> dict:
        """
        Search the web using Brave Search API and return results as a dict.

        Args:
            query: The search query string
            count: Number of search results to fetch (default 3)

        Returns:
            A dictionary containing search results or an 'error' key if the request failed
        """
        params = {
            "q": query,
            "count": count
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MyAgent/1.0)",
            "X-Subscription-Token": os.getenv("BRAVE_SEARCH_API")
        }

        try:
            response = httpx.get(BRAVE_SEARCH_API_URL, params=params, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            return {"error": f"Error fetching Brave Search results: {e}"}
        
    brave_search = tool(parse_docstring=True)(brave_search_fn)
    


    
        
        