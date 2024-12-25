from enum import StrEnum
import time
from typing import Any, Dict, List
import requests

import xmltodict


class AuthorDoesNotExistError(Exception):
    pass


class SearchType(StrEnum):
    PUBLICATION= "https://dblp.org/search/publ/api"
    AUTHOR= "https://dblp.org/search/author/api"
    VENUE = "https://dblp.org/search/venue/api"


class ResultFormat(StrEnum):
    JSON = "json"
    XML = "xml"
    JSONP = "jsonp"


def search_dblp(
    query: List[str], 
    search_type: SearchType = SearchType.PUBLICATION,
    format: ResultFormat = ResultFormat.JSON,
    max_results: int = 1000, 
    max_completion_terms: int = 1000
):
    """
    Construct a search query based on https://dblp.org/faq/How+to+use+the+dblp+search+API.html
    """
    if isinstance(query, str):
        query = query.split(" ")
    assert isinstance(query, list), f"Query must be a list of terms but got {query}"
    url = construct_search_url(
        query_terms=query,
        search_type=search_type,
        format=format,
        max_results=max_results,
        max_completion_terms=max_completion_terms,
    )
    response = requests.get(url)
    if response.status_code == 429:
        raise ConnectionError(f"Request rejected due to too many requests")
    else:
        hits = response.json()["result"]["hits"]
        if int(hits["@total"]) == 0:
            raise AuthorDoesNotExistError(f"Could not find results for author {query} in dblp")
        return hits["hit"]


def construct_search_url(
    query_terms: List[str], 
    search_type: SearchType,
    format: ResultFormat = ResultFormat.JSON,
    max_results: int = 1000, 
    max_completion_terms: int = 1000,
):
    query = "+".join(query_terms)
    url = f"{search_type.value}?q={query}&format={format.value}&c={max_completion_terms}&h={max_results}"
    return url


def get_publications(name: str, sleep_duration: int = 1) -> List[Dict[str, Any]]:
    data = get_dblp_publication_response(name=name, sleep_duration=sleep_duration)
    # publications are wrapped in a dictionary like
    # {"inproceedings": {<content>}} or {"article": {<content>}}
    results = data["dblpperson"]["r"]
    results = results if isinstance(results, list) else [results]
    publications = [tuple(p.values())[0] for p in results]
    return publications


def get_dblp_publication_response(name: str, sleep_duration: int = 1) -> List[Dict[str, Any]]:
    author = search_dblp(
        query=name, 
        search_type=SearchType.AUTHOR,
        max_completion_terms=10,
    )[0]
    time.sleep(sleep_duration)
    url = f"{author["info"]["url"]}.xml"

    author_reponse = requests.get(url)
    if author_reponse.status_code == 429:
        raise ConnectionError("Too many requests")
    data = xmltodict.parse(author_reponse.text)
    return data
