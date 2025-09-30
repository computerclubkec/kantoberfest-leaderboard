import gspread
from gspread_dataframe import get_as_dataframe
import pandas as pd
from typing import List


def _extract_data_from_sheets(api_key: str, sheet_id: str) -> pd.DataFrame:
    """
    Extract data from Google Sheets and return as a pandas DataFrame.

    Args:
        api_key: Google Sheets API key
        sheet_id: ID of the Google Sheet

    Returns:
        DataFrame containing the sheet data
    """
    gc = gspread.api_key(token=api_key)
    wks = gc.open_by_key(sheet_id).sheet1
    df = get_as_dataframe(wks)
    # Ensure we return a DataFrame, not a Series
    if isinstance(df, pd.Series):
        df = df.to_frame()
    return df


def _get_user_names(df: pd.DataFrame) -> List[str]:
    profile_links = df["Github Profile Link"]
    usernames = []
    for link in profile_links:
        if pd.isna(link):
            continue
        link = str(link).strip()
        if link.startswith("https://github.com/"):
            username = link.replace("https://github.com/", "")
        elif link.startswith("github.com/"):
            username = link.replace("github.com/", "")
        elif link.startswith("www.github.com/"):
            username = link.replace("www.github.com/", "")
        else:
            username = link

        # Remove any trailing slashes and clean up
        username = username.rstrip("/")
        if username:
            usernames.append(username)

    return usernames


def get_users_list(api_key: str, sheet_id: str) -> List[str]:
    df = _extract_data_from_sheets(api_key, sheet_id)
    usernames = _get_user_names(df)
    return usernames
