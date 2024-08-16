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

import asyncio
import tornado
import csv

class MainHandler(tornado.web.RequestHandler):
    """MainHandler handles requests to the server/API.

    Given a request like this:

    http://localhost:8888/?xyz=123&abc=456

    the get() method pulls xyz=123&abc=456 into the variable api_request

    Feel free to add additional methods, create other classes, etc.
    """

    def get(self):
        api_request = self.request.query

        # Write back the api request to the browser, for convenience.
        self.write(api_request)

        ### Do stuff with the api request ###

def read_db():
    """Reads the article database and returns a reader object with the data"""
    with open('articlesembeds.csv', newline='') as csvfile:
        articlereader = csv.reader(csvfile, delimiter=';')
        return articlereader

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

async def main():
    app = make_app()
    app.listen(8888)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())