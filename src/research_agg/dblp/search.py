from enum import StrEnum
from typing import List
import requests


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
    return response.json()["result"]["hits"]["hit"]


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