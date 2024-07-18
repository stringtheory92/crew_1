# tasks:
#   - name: ScrapeArticlesTask
#     description: Scrape articles and gather initial data
#     agent: ResearcherAgent
#     tools:
#       - WebScraper
#     expected_output: List of articles with titles, links, and summaries
#     next: AnalyzeArticlesTask

#   - name: AnalyzeArticlesTask
#     description: Analyze articles to find new features/products
#     agent: ResearcherAgent
#     expected_output: Compiled list of features/products in a bulleted list
#     next: CompileFeatureListTask

#   - name: CompileFeatureListTask
#     description: Compile the list of features/products into a detailed bulleted list
#     agent: ResearcherAgent
#     expected_output: Detailed bulleted list of AI/ML features and products
#     next: HandoffToWriterTask

#   - name: HandoffToWriterTask
#     description: Hand off the compiled list to the WriterAgent
#     agent: ResearcherAgent
#     expected_output: Notification to WriterAgent with compiled data
#     next: WriteContentTask

#   - name: WriteContentTask
#     description: Write detailed, engaging content based on the compiled list
#     agent: WriterAgent
#     expected_output: Engaging article or report on new AI/ML features and products

import os
from crewai import Agent, Task, Crew

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    SerperDevTool,
    WebsiteSearchTool,
    ScrapeWebsiteTool
)

docs_tool = DirectoryReadTool(directory='./blog-posts')
file_tool = FileReadTool()
search_tool = SerperDevTool()
web_rag_tool = WebsiteSearchTool()
web_scraper_tool = ScrapeWebsiteTool()

# software_developer = Agent(
#     role='Software Developer',
#     goal='Follow a link to an article from the database. Analyze the HTML structure to find the main text. Write an HTML parsing function using BeautifulSoup. Pass the extracted text to the ResearcherAgent.',
#     backstory=' The SoftwareDeveloperAgent is an AI expert in web scraping and HTML analysis. It can quickly understand and navigate HTML structures to extract relevant data. The agent is highly skilled in Python and BeautifulSoup, making it an essential part of the data extraction process.'
# )

researcher = Agent(
    role='AI Product Researcher',
    goal='Analyze un-analyzed links in the articles database. Gather all relevant information about AI/ML features and products. Compile the information into JSON format: { product { product_details, features { feature_name { feature_details } } } }. For new product_details and feature_details for features/products already in the database, insert a new row in the db for each new detail in the relevant table, with . For a new product/feature, insert a new row for the new product/feature in the relevant table',
    # goal='Analyze un-analyzed links in the articles database. Gather all relevant information about AI/ML features and products. Compile the information into JSON format: { product { product_details, features { feature_name { feature_details } } } }. Hand off the compiled information to the WriterAgent.',
    backstory='The ResearcherAgent is an AI specialized in identifying, analyzing, and compiling information about features and products in the AI and machine learning domains, It has been trained on a vast dataset of AI and machine learning resources and is adept at discerning valuable insights from technical content, The agent is meticulous and thorough, ensuring that all relevant information is gathered and presented in a clear, concise manner.',
    tools=[web_rag_tool, web_scraper_tool]
)

writer = Agent(
    role='AI Content Writer',
    goal='Receive the compiled list of features/products from the ResearcherAgent. Create detailed, engaging write-ups based on the provided information. Ensure that the content is accessible to both technical and non-technical audiences. Export result as txt file.',
    backstory='The WriterAgent is an AI skilled in content creation, particularly in the field of AI and machine learning. It has a background in technical writing and journalism, with a knack for making complex topics understandable and interesting. The agent works closely with the ResearcherAgent to produce high-quality content that informs and educates its audience.',
    tools=[docs_tool, file_tool]
)

