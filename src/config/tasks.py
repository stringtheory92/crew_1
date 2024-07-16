# tasks:
#   - name: ScrapeArticlesTask
#     description: Scrape articles and gather initial data
#     agent: ResearcherAgent
#     tools:
#       - WebScraper
#     expected_output: List of articles with titles, links, and summaries

#   - name: AnalyzeArticlesTask
#     description: Analyze articles to find new features/products
#     agent: ResearcherAgent
#     expected_output: Compiled list of features/products in a bulleted list
#     context: ScrapeArticlesTask

#   - name: CompileFeatureListTask
#     description: Compile the list of features/products into a detailed bulleted list
#     agent: ResearcherAgent
#     expected_output: Detailed bulleted list of AI/ML features and products
#     context: AnalyzeArticlesTask

#   - name: HandoffToWriterTask
#     description: Hand off the compiled list to the WriterAgent
#     agent: ResearcherAgent
#     expected_output: Notification to WriterAgent with compiled data
#     context: CompileFeatureListTask

#   - name: WriteContentTask
#     description: Write detailed, engaging content based on the compiled list
#     agent: WriterAgent
#     expected_output: Engaging article or report on new AI/ML features and products
#     context: HandoffToWriterTask

from crewai import Task
from crewai_tools import ScrapeWebsiteTool

web_scraper_tool = ScrapeWebsiteTool()


ScrapeArticlesTask = Task(
 description: Scrape articles and gather initial data
    agent='researcher'
    tools=[web_scraper_tool]
    expected_output: List of articles with titles, links, and summaries   
)