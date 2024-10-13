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
* Do one/two thing(s) well (easy startup, recommend). Let humans do the rest, for now
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

import tornado

from  recommenado.recommend import recommend

# TODO: Extend Tornado's default logger
LOG: logging.Logger = logging.getLogger(name="Recommenado") 

class MainHandler(tornado.web.RequestHandler):
    """
    Handler to recieve requests and direct users around the app
    """

    def get(self):
        LOG.critical("MainHandler get request")
        self.set_status(200)
        self.write("<p>Welcome to Recommenado, a tool to empower readers to be as fully informed as they'd like to be in areas they're most concerned about.</p>")
        self.write("<p>Navigate to /recommend to get article recommendations via form</p>")
        self.write("<p>Navigate to /recommend_api to get article recommendations via HTTP request</p>")
        self.write("<p>Navigate to /upload to add articles to the recommendation database (not implemented yet!)</p>")

class RecommendationAPIHandler(tornado.web.RequestHandler):
    async def get(self):
        """
        API endpoint to recieve related article recommendations

        For now, users will upload article title and text in the form of
        search query params, e.g., 
        http://localhost:8888/recommend_api?article_headline=123&article_text=456
        """
        LOG.critical("RecommendationAPIHandler get request")
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
        LOG.critical("RecommendationAPIHandler post request")
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
        """
        Recieve HTTPS form data and return article recommendations
        """
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
    