""" Fetch contributions for multiple users """

import json
import logging
import pandas as pd
from typing import Dict

from leaderboard.queries.query import query
from leaderboard.fetch_data import execute_query
from leaderboard.utils.formatter import convert_to_intermediate_table

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fetch_data")


def fetch_contributions_for_multi_users(
    user_list: list, query_variables: Dict
) -> pd.DataFrame:
    """
    Fetches contribution data for multiple GitHub users and returns a combined intermediate table dataframe.

    Args:
        user_list (list): List of GitHub usernames whose contribution data is to be fetched.
        query_variables (Dict): Arguments required for the OSS graphql query.

    Returns:
        pd.DataFrame: Combined intermediate table dataframe for all users.
    """
    # stores list of intermediate dataframes
    intermediate_list = []

    for userName in user_list:
        query_variables["username"] = userName
        # variables that sore the pagination info for each of the 5 contribution types
        page_info_T1 = {"hasNextPage": True, "endCursor": None}

        page_info_T2 = {"hasNextPage": True, "endCursor": None}

        page_info_T3 = {"hasNextPage": True, "endCursor": None}

        # in case of issue comment(T4), 'hasPreviousPage' and 'startCursor' is used instead as it involves a different approach to get issue comment contributions after a specific time
        page_info_T4 = {"hasPreviousPage": True, "startCursor": None}

        page_info_T5 = {"hasNextPage": True, "endCursor": None}

        while True:
            # extra params required for pagination
            query_variables["pullReqCursor"] = page_info_T1["endCursor"]

            query_variables["pullreqreviewcursor"] = page_info_T2["endCursor"]

            query_variables["issueCursor"] = page_info_T3["endCursor"]

            query_variables["issueCommentsCursor"] = page_info_T4["startCursor"]

            query_variables["repoCursor"] = page_info_T5["endCursor"]

            # in case of issue comment(T4), if 'hasPreviousPage' is false, we set the data count to zero so that no more issue comment data is fetched
            if page_info_T4["hasPreviousPage"]:
                query_variables["issueCommentDataCount"] = query_variables["dataCount"]
            else:
                query_variables["issueCommentDataCount"] = 0

            result = execute_query(query, query_variables)

            user = result.json()["data"]["user"]
            if user == None:
                logger.info("Invalid GitHub user detected %s\n", userName)
                break

            flat_data = convert_to_intermediate_table(
                json.dumps(result.json(), indent=4), query_variables["timedelta"]
            )

            intermediate_list.append(flat_data["intermediate_table"])

            # we only set the page info values that we get from api response when the hasNextPage/hasPreviousPage is true
            # once we get a false value for hasNextPage/hasPreviousPage from api, we set the page info once and ignore the page info value in subsequent responses
            if page_info_T1["hasNextPage"]:
                page_info_T1 = flat_data["page_info"]["page_info_T1"]

            if page_info_T2["hasNextPage"]:
                page_info_T2 = flat_data["page_info"]["page_info_T2"]

            if page_info_T3["hasNextPage"]:
                page_info_T3 = flat_data["page_info"]["page_info_T3"]

            if page_info_T4["hasPreviousPage"]:
                page_info_T4 = flat_data["page_info"]["page_info_T4"]

            if page_info_T5["hasNextPage"]:
                page_info_T5 = flat_data["page_info"]["page_info_T5"]

            # if none of the contribution data types have any more data to be fetched for a user, break out of the whie loop and move on to next user
            if (
                not page_info_T1["hasNextPage"]
                and not page_info_T2["hasNextPage"]
                and not page_info_T3["hasNextPage"]
                and not page_info_T4["hasPreviousPage"]
                and not page_info_T5["hasNextPage"]
            ):
                break

    # combines all the intermediate dataframes into one
    combined = pd.concat(intermediate_list)

    return combined
