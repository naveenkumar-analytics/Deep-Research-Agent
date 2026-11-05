import asyncio
from agents import Runner
from search_agent import search_agent
from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent, ReportData
from email_agent import email_agent


class ResearchManager:

    async def run(self, query: str):
        """Run the deep research process, yielding status updates and the final report"""
        yield "Starting research..."
        search_plan = await self.plan_searches(query)
        yield f"Searches planned, starting {len(search_plan.searches)} searches..."
        search_results = await self.perform_searches(search_plan)
        yield "Searches complete, writing report..."
        report = await self.write_report(query, search_results)
        yield "Report written, sending email..."
        email_status = await self.send_email(report)
        yield email_status
        yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        result = await Runner.run(planner_agent, f"Query: {query}")
        return result.final_output

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        results = []
        for item in search_plan.searches:      # ek ek karke, free limit ke liye
            results.append(await self.search(item))
            await asyncio.sleep(2)
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        input_message = f"Search term: {item.query}\nReason for searching: {item.reason}"
        result = await Runner.run(search_agent, input_message)
        return result.final_output

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        input_message = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output

    async def send_email(self, report: ReportData) -> str:
        result = await Runner.run(email_agent, report.markdown_report)
        for item in result.new_items:
            if type(item).__name__ == "ToolCallOutputItem":
                output = str(item.output)
                if "successfully" in output:
                    return "Email sent, research complete"
                return f"Email FAILED: {output}"
        return "Email was not sent (the agent did not call the email tool)"