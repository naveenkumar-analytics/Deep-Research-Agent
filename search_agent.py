from agents import Agent, ModelSettings, function_tool
from ddgs import DDGS
from gemini_config import gemini_model


@function_tool
def web_search(query: str) -> str:
    """Search the web and return titles, URLs and snippets for the query."""
    results = DDGS().text(query, max_results=5)
    return "\n\n".join(f"{r['title']}\n{r['href']}\n{r['body']}" for r in results)


INSTRUCTIONS = """
You are a research assistant. Given a search term, you search the web for that term and 
produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 words.
Capture the main points and be succinct. Reply only with the summary.
"""

settings = ModelSettings(tool_choice="required")

search_agent = Agent(
    name="Search Agent",
    instructions=INSTRUCTIONS,
    tools=[web_search],
    model=gemini_model,
    model_settings=settings,
)