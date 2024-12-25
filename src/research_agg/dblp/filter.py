from typing import Any, Callable, Dict, List, Optional


def filter_results(
    results: List[Dict[str, Any]], 
    filter_fn: Callable[[Dict[str, Any]], bool]
) -> List[Dict[str, Any]]:
    return [r for r in results if filter_fn(r)]


def filter_publication_by_year(
    results: List[Dict[str, Any]], 
    min_year: Optional[int] = None, 
    max_year: Optional[int] = None,
) -> List[Dict[str, Any]]:
    filter_fn = get_publication_year_filter_fn(min_year=min_year, max_year=max_year)

    return filter_results(results, filter_fn=filter_fn)


def get_publication_year_filter_fn(min_year: Optional[int] = None, max_year: Optional[int] = None):
    def filter_fn(r: Dict[str, Any]) -> bool:
        year = int(r["year"])
        return (min_year is None or year >= min_year) and (max_year is None or year <= max_year)
    return filter_fn


def get_affiliation_filter_fn(
    whitelist: Optional[List] = None,
    blacklist: Optional[List] = None,
) -> Callable:
    whitelist = set() if whitelist is None else set([w.lower() for w in whitelist])
    blacklist = set() if blacklist is None else set([b.lower() for b in blacklist])
    def filter_fn(name: str, affiliation: str) -> bool:
        affiliation = affiliation.lower()
        return affiliation in whitelist and affiliation not in blacklist
    return filter_fn
    
