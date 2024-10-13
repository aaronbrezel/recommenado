#!/usr/bin/env python3
"""Local News Lab Tech Lead At-home Task start module.

We use the Tornado web server for our article recommendations API.
https://www.tornadoweb.org/en/stable/index.html

Please start your Tornado web app with this file. But feel free to modify this
file as much as you'd like and to create additional modules if you'd like.

Currently, this setup assumes a simple API request like this:

http://localhost:8888/?xyz=123&abc=456

But please modify the API request format as much as you'd like.

Note that we've included the function read_db() to retrieve the data from
articlesembeds.csv, which is our article "database". There are 4 rows of data.
There are two columns in this "database":
Article ID
Embedding (from Google's Gemini API)

Please use the RequestHandler write() method to return the API response.
This will write it to the browser and make it easy for us to see how you're
structuring the response.

Again, we're kindly requesting only 2 to 3 hours of your time. If you'd like, you
can note areas where you'd expand or do things differently with more time and
resources. This is a conversation starter to show us how you think and work!

Please feel free to contact me (Eric) with any questions:
eric.evan.chen@columbia.edu

Have fun! =)
"""

"""
Implementation notes:
* Two problems here: 
    * recommendation algorithm
    * Connecting low tech newsroom to tool 
* Aim for person in the newsroom who can write a python script
* Modular, extendable
* Low touch. Small team == less time for tech support. Documentation, FAQs, etc.
* As lightweight as possible: 
    * < dependencies
    * > runtime flexibility
    * < failure points
* Do one thing well (recommend). Let humans do the rest, for now
* Pip installable, Docker image, etc.
* Forkable from git. Open sourced and encourage PRs
* Self hosted is preferrable. Perhaps run locally. Removes need for auth flow, scaling, etc. 

Future looking improvements:
* Upload articles via form or flat files w/ easily customizable ingest function (match newsroom article format to SQL server)
* SQLite w/ its sharable filesystem is ideal over heavier Postgres or MySQL
* Consider using https://github.com/asg017/sqlite-vec to provide a lightweight vector extension
* Recommendations might improve with RAG (retrieval augmented generation) or cohere rerank API


How will you structure requests from the newsroom to the API?
* Search can be done through html form (less technical) or http request (more technical)
* Human readable form data

How one more more articles is recommended?
* L2Distance, CosineDistance, KNN?
* RAG, Rerank
* prompt engineering could help fine-tune recommendations ("Give me results about hurricanes")

How will you structure responses back to the newsroom?
* JSON response or simple html list elements
* return similarity score -- try to provide window into black box
"""

import asyncio
import logging
import json

import tornado

from  recommenado.recommend import recommend

# TODO: Extend Tornado's default logger
LOG: logging.Logger = logging.getLogger(name="Recommenado") 

class MainHandler(tornado.web.RequestHandler):
    """
    Handler to recieve requests and direct users around the app
    """

    def get(self):
        self.set_status(200)
        self.write("Welcome to Recommenado, a tool to empower readers to be as fully informed as they'd like to be in areas they're most concerned about.")
        self.write("Navigate to /recommend to get article recommendations via form")
        self.write("Navigate to /recommend_api to get article recommendations via HTTP request")
        self.write("Navigate to /upload to add articles to the recommendation database")

class RecommendationAPIHandler(tornado.web.RequestHandler):
    async def get(self):
        """
        API endpoint to recieve related article recommendations

        For now, users will upload article title and text in the form of
        search query params, e.g., 
        http://localhost:8888/recommend_api?article_headline=123&article_text=456

        """
        article_headline = self.get_query_argument('article_headline', default=None)
        article_text = self.get_query_argument('article_text', default=None)

        # Write back the api request to the browser, for convenience.
        recommendations = recommend(article_headline, article_text)
        self.set_status(200)
        self.write("Eureka! Here are your matches:")
        self.write(str(recommendations))
        
    async def post(self):
        """
        API endpoint to recieve related article recommendations

        In the future, I'd like to make recommendations accessible via 
        non-browser http post requests, e.g., curl
        """
        self.set_status(200)
        self.write("Not Implemented yet!")


class RecommendationFormHandler(tornado.web.RequestHandler):
    async def get(self):
        """
        HTML Form to recieve related article recommendations. 
        
        For now, lets assume users will upload plain text, but this form may expand 
        into files or other metadata in the future pending search algorithm development
        """
        LOG.critical("RecommendationFormHandler get request")
        self.set_status(200)
        self.write('<html><body><p>You give me text, I give you article recommendations</p><br>'
                   '<form action="/recommend" method="POST">'
                   '<input type="text" placeholder="Headline" name="article_headline">'
                   '<input type="text" placeholder="Body" name="article_text">'
                   '<input type="submit" value="Submit">'
                   '</form></body></html>')
    async def post(self):
        LOG.critical("RecommendationFormHandler post request")
        
        # Get article headline and text from request
        article_headline: str = self.get_body_argument('article_headline')
        article_text: str = self.get_body_argument('article_text')
        recommendations = recommend(article_headline, article_text)
        self.set_status(200)
        self.write("Eureka! Here are your matches:")
        self.write(str(recommendations))

class UploadHandler(tornado.web.RequestHandler):
    async def get(self):
        LOG.critical("UploadHandler get request")
        self.write("Not implemented yet!")
    async def post(self):
        """
        Recieve upload text, embed it, and add it to the database of embedded articles
        """
        LOG.critical("UploadHandler post request")
        self.write('Not implemented yet!')

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/recommend", RecommendationFormHandler),
        (r"/recommend_api", RecommendationAPIHandler),
        (r"/upload", UploadHandler),
    ], debug=True)

async def run_server():
    LOG.critical("Starting sever ...")
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

def main():
    asyncio.run(run_server())
    