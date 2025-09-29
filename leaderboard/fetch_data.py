""" Fetch required data from the GitHub API. """
import os
import json
import logging
from typing import Dict

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fetch_data")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
API_ENDPOINT = "https://api.github.com/graphql"

headers = {"Authorization": "token " + GITHUB_TOKEN}

logger.info(headers)


def execute_query(query: str, variables: Dict) -> requests.models.Response:
    """
    Executes query to fetch data from GraphQL API.

    Args:
        query (str): GraphQL query for fetching data.
        variables (Dict): Variables to be used in the GraphQL query.

    Returns:
        requests.models.Response: Response object containing the fetched data.

    Raises:
        Exception: If the request fails with a non-200 status code.
    """

    s = requests.Session()

    retries = Retry(
        total=5,
        backoff_factor=0.8,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=(["POST"]),
    )

    s.mount("https://", HTTPAdapter(max_retries=retries))

    request = s.post(
        url=API_ENDPOINT,
        json={"query": query, "variables": variables},
        headers=headers,
        timeout=20,
    )

    if request.status_code == 200:
        logger.info(json.dumps(request.json(), indent=4))

        return request

    else:
        raise Exception(
            "Request failed with code of {} \n{}.".format(
                request.status_code, request.text
            )
        )
