""" Main module for the OSS Leaderboard. """
import os
import logging

from leaderboard.utils.intermediate_score_table import get_intermediate_score_table
from leaderboard.utils.final_score_table import get_final_score_table
from leaderboard.utils.get_users import get_users_list
from multi_users_fetch import fetch_contributions_for_multi_users
from final_html_output import final_html_output
from leaderboard.utils.data import remove_duplicates_case_insensitive

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("main")

# Form bata data taani
duration = int(os.environ.get("DURATION_IN_DAYS", 5))
data_count = int(os.environ.get("PAGE_DATA_COUNT", 5))
start_date = os.environ.get("START_DATE", "2023-10-01T00:00:00")
google_sheets_api_key = os.environ.get("GOOGLE_SHEETS_API_KEY", "")
google_sheets_id = os.environ.get("GOOGLE_SHEETS_ID", "")

if google_sheets_api_key and google_sheets_id:
    user_list = get_users_list(google_sheets_api_key, google_sheets_id)
else:
    user_list = [x.strip() for x in os.environ.get("USER_LIST", "").split(",")]


variables = {
    "timedelta": start_date,
    "dataCount": data_count,
}


def main():
    """Script entrypoint.

    This function fetches contributions for multiple users, calculates their scores, and generates an HTML output of the final leaderboard.

    Returns:
        None
    """

    # Remove duplicate usernames.
    dedup_user_list = remove_duplicates_case_insensitive(user_list)

    result = fetch_contributions_for_multi_users(dedup_user_list, variables)

    intermediate_score_table = get_intermediate_score_table(result)
    final_score_table = get_final_score_table(intermediate_score_table, dedup_user_list)

    final_html_output(final_score_table)


main()
