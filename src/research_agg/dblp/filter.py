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
    def filter_fn(r: Dict[str, Any]) -> bool:
        year = int(r["year"])
        return (min_year is None or year >= min_year) and (max_year is None or year <= max_year)

    return filter_results(results, filter_fn=filter_fn)
