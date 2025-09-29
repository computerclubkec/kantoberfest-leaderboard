""" Utilities for data processing. """
from datetime import datetime, timedelta
import pandas as pd
import markdown


def get_date(days: int) -> str:
    """
    Get date before x days.

    Args:
        days (int): Number of days before from which data is fetched.

    Returns:
        str: DateTime string in isoformat.
    """
    return (datetime.today() - timedelta(days=days)).isoformat()


def convert_df_to_markdown(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to a markdown table.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: The markdown table as a string.
    """
    return df.to_markdown()


def convert_df_to_html(df: pd.DataFrame) -> str:
    """
    Convert a pandas DataFrame to an HTML table.

    Args:
        df (pd.DataFrame): The DataFrame to convert.

    Returns:
        str: The HTML string representing the DataFrame as a table.
    """
    return df.to_html()


def convert_mk_to_html(mk_data: str) -> str:
    """
    Convert markdown to html.

    Args:
        mk_data (str): The markdown string to convert.

    Returns:
        str: The resulting html string.
    """
    return markdown.markdown(mk_data, extensions=["tables"])


def remove_duplicates_case_insensitive(input_list):
    """
    Remove duplicate entries from a list case insensitively.

    Args:
        input_list (list): The list from which to remove duplicates.

    Returns:
        list: A new list containing the unique items from the input list,
              preserving the case of the first occurrence of each item.
    """
    # Create a set to track unique lowercase versions of the list items
    seen = set()
    result = []

    for item in input_list:
        lower_item = item.lower()
        if lower_item not in seen:
            seen.add(lower_item)
            result.append(item)

    return result
