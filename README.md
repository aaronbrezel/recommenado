# Recommenado

Welcome to Recommenado! It's a light weight, run-anywhere article recommendation tool. Install the Python package, get an API key, and get started. 

This package is under active development, so check back often for new features and tools. Or, fork this repo and make your own improvements! 

## Quickstart

### Clone repo

```
git clone https://github.com/aaronbrezel/recommenado.git
```

### Python env

Recommenado is best run in a dedicated python virtual environment. We like [pyenv](https://github.com/pyenv/pyenv), but any virtual env will do.

```
pyenv virtualenv 3.12 recommenado
pyenv activate recommenado
```

### Install

Install Recommenado into your newly created virtual environment
```
pip install -e .
```

*Developer's note: Recommanado's source code is meant to be run locally, tweaked and played with. That's why we encorage you to install it in [editable mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#development-mode-a-k-a-editable-installs). If you want a "production" version of the application, see [Docker start](#docker-start)*

### Generate Google GenAI API key

You'll need a [Google GenAI](https://ai.google.dev/gemini-api/docs) API key to help generate recommendations. Use [this link](https://aistudio.google.com/app/apikey) to get your personal API key. Once you have it, navigate over to [./recommenado/recommend/model.py](./recommenado/recommend/model.py) and paste the value into `genai.configure(api_key="<your api key goes here>")`. 

*Developer's note: this API key is your responsibility. [Keep it secret, keep it safe](https://towardsdatascience.com/how-you-can-and-why-you-should-secure-your-api-keys-e433acc2f22d). Only share it with people you trust. And for the love of all that is holy, do not commit it to a public GitHub repository.*

### Upload

For now, Recommenado's backend database consists of a single `;`-separated `.csv` file located at [./recommenado/recommend/articlesembeds.csv](./recommenado/recommend/articlesembeds.csv). 

The file consists of two tabular columns: article title and article embedding.

To upload articles to the recommendation database, add rows to the csv. Embeddings can be generated à la carte using the following script:

```Python
import google.generativeai as genai
genai.configure(api_key="<your api key goes here>")
text = '<your article text here>'
embedding = genai.embed_content(model='models/text-embedding-004', content=text, task_type='models/text-embedding-004')['embedding']
print(embedding)
```

*Developer's note: we're working on a smoother article database upload experience that does not require directly editing a `.csv` file.*

### Run!

Start the recommenado server
```
recommenado
```

### Recommenado!

[http://localhost:8888/recommend_api?article_title=hello&article_text=world](http://localhost:8888/recommend_api?article_title=hello&article_text=world)

or 

[http://localhost:8888/recommend](http://localhost:8888/recommend)


## Docker start

TK!