from recommenado.recommend.model import semantic_match

def recommend(title: str, text: str) -> list:
    """
    Given an article title and text, return n number of 
    article recommendations

    Essentially a light wrapper around model.semantic_match function
    in order to allow us to swap out the recommendation algorithm easily

    I'm starting with "semantic" recommendations as it appears to fit our use case
    of readers wanting to read articles similar in content to the one they just read

    Semantic search does not require article "title", but it can be used for other retrieval tasks,
    (RAG, prompt engineering, etc.), so I'm going to leave that in for now as a nod
    
    recommendation strategy drawn heavily from https://ai.google.dev/gemini-api/tutorials/document_search 
    """

    matches: list = semantic_match(text)
    # Cast data structure into human readable format
    matches = [{'article': match['article'], 'distance': round(float(match['distance']), 3)} for match in matches]
    return matches