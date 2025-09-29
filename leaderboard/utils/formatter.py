""" Util to convert the json to dataframe. """

import json
from typing import Dict, List

import pandas as pd
from leaderboard.constants import contribTypes


def convert_to_intermediate_table(data: str, timeDelta: str) -> pd.DataFrame:
    """
    Converts a JSON string containing data about a user's contributions on GitHub
    into an intermediate table format that can be used to generate a leaderboard.

    Args:
        data (str): A JSON string containing data about a user's contributions on GitHub.
        timeDelta (str): A string representing a time delta in the format "X days/hours/minutes".

    Returns:
        dict: A dictionary containing two keys:
            - "intermediate_table": A pandas DataFrame containing the intermediate table.
            - "page_info": A dictionary containing pagination information for the API query.
    """
    df = pd.DataFrame.from_dict(
        pd.json_normalize(json.loads(data.encode())), orient="columns"
    )

    user_github_id = df["data.user.id"][0]
    user_name = df["data.user.username"][0]
    issue_comment_list = df["data.user.issueComments.edges"][0]
    review_contribution_list = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.edges"
    ][0]
    pr_contribution_list = df[
        "data.user.contributionsCollection.pullRequestContributions.edges"
    ][0]
    issue_contribution_list = df[
        "data.user.contributionsCollection.issueContributions.edges"
    ][0]
    repo_contribution_list = df[
        "data.user.contributionsCollection.repositoryContributions.edges"
    ][0]

    new_df = pd.DataFrame(
        columns=[
            "github_id",
            "user_id",
            "user_name",
            "type",
            "repo_id",
            "repo_owner_id",
            "pr_status",
            "label",
            "commits",
            "review_type",
            "forks",
            "stars",
            "comments",
            "reactions",
            "merged_by_id",
            "author_id",
            "is_fork",
            "created_at",
            "last_updated_at",
        ]
    )

    new_df = format_pr_review_contributions(
        review_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_pr_contributions(
        pr_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_issue_contributions(
        issue_contribution_list, user_github_id, user_name, new_df
    )
    new_df = format_repo_contributions(
        repo_contribution_list, user_github_id, user_name, new_df
    )
    new_df_info = format_issue_comments(
        issue_comment_list, user_github_id, user_name, timeDelta, new_df
    )

    page_info = extract_page_info(df)

    # in case of issue comment(T4), we calculate the value for hasPreviousPage
    # based on whether the latest api response has any issue comment contribution data that was created before the specified time
    page_info["page_info_T4"]["hasPreviousPage"] = (
        not new_df_info["hasOldData"] and page_info["page_info_T4"]["hasPreviousPage"]
    )

    return {"intermediate_table": new_df_info["df"], "page_info": page_info}


def extract_page_info(df: pd.DataFrame) -> Dict:
    """
    Returns page info for each of the contribution types

    Args:
        df: graphql query api response converted to dataframe

    Returns:
        A dictionary containing page info for each of the contribution types
    """

    has_next_page_T1 = df[
        "data.user.contributionsCollection.pullRequestContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T1 = df[
        "data.user.contributionsCollection.pullRequestContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T2 = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T2 = df[
        "data.user.contributionsCollection.pullRequestReviewContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T3 = df[
        "data.user.contributionsCollection.issueContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T3 = df[
        "data.user.contributionsCollection.issueContributions.pageInfo.endCursor"
    ][0]

    has_next_page_T4 = df["data.user.issueComments.pageInfo.hasPreviousPage"][0]
    end_cursor_T4 = df["data.user.issueComments.pageInfo.startCursor"][0]

    has_next_page_T5 = df[
        "data.user.contributionsCollection.repositoryContributions.pageInfo.hasNextPage"
    ][0]
    end_cursor_T5 = df[
        "data.user.contributionsCollection.repositoryContributions.pageInfo.endCursor"
    ][0]

    return {
        "page_info_T1": {
            "hasNextPage": has_next_page_T1,
            "endCursor": end_cursor_T1,
        },
        "page_info_T2": {
            "hasNextPage": has_next_page_T2,
            "endCursor": end_cursor_T2,
        },
        "page_info_T3": {
            "hasNextPage": has_next_page_T3,
            "endCursor": end_cursor_T3,
        },
        "page_info_T4": {
            "hasPreviousPage": has_next_page_T4,
            "startCursor": end_cursor_T4,
        },
        "page_info_T5": {
            "hasNextPage": has_next_page_T5,
            "endCursor": end_cursor_T5,
        },
    }


def format_issue_comments(
    issue_comment_list: str,
    user_id: str,
    user_name: str,
    timeDelta: str,
    df: pd.DataFrame,
) -> Dict:
    """
    Formats a list of issue comments and appends them to a pandas DataFrame.

    Args:
        issue_comment_list (str): A list of issue comments.
        user_id (str): The ID of the user who made the comments.
        user_name (str): The name of the user who made the comments.
        timeDelta (str): A string representing the time delta for filtering comments.
        df (pd.DataFrame): A pandas DataFrame to which the formatted comments will be appended.

    Returns:
        dict: A dictionary containing the updated DataFrame and a boolean indicating whether there are older comments.
    """
    olderDataCount = 0

    for issue_comment in issue_comment_list:
        github_id = issue_comment["node"]["id"]
        repo_id = issue_comment["node"]["issue"]["repository"]["id"]
        repo_owner_id = issue_comment["node"]["issue"]["repository"]["owner"]["id"]
        reactions = issue_comment["node"]["issue"]["reactions"]["totalCount"]
        created_at = issue_comment["node"]["createdAt"]
        last_updated_at = issue_comment["node"]["updatedAt"]

        if created_at >= timeDelta:
            df = df.append(
                {
                    "github_id": github_id,
                    "user_id": user_id,
                    "user_name": user_name.lower(),
                    "type": contribTypes.T4,
                    "repo_id": repo_id,
                    "repo_owner_id": repo_owner_id,
                    "reactions": reactions,
                    "created_at": created_at,
                    "last_updated_at": last_updated_at,
                },
                ignore_index=True,
            )
        else:
            olderDataCount += 1

    return {"df": df, "hasOldData": olderDataCount > 0}


def format_pr_review_contributions(
    review_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats pull request review contributions and appends them to a pandas DataFrame.

    Args:
        review_contribution_list (List): A list of pull request review contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """
    for pr_review in review_contribution_list:
        github_id = pr_review["node"]["pullRequestReview"]["id"]
        pr_review_node = pr_review["node"]["pullRequestReview"]
        repo_id = pr_review["node"]["repository"]["id"]
        repo_owner_id = pr_review["node"]["repository"]["owner"]["id"]

        review_type = pr_review_node["ReviewState"]
        pr_status = pr_review_node["pullRequest"]["state"]

        author_id = ""
        if pr_review_node["pullRequest"]["author"]:  # handle deleted user
            author_id = pr_review_node["pullRequest"]["author"].get("id")

        reactions = pr_review_node["reactions"]["totalCount"]
        merged_by_id = ""

        if pr_review_node["pullRequest"]["merged"]:
            merged_by_id = pr_review_node["pullRequest"]["mergedBy"]["login"]

        created_at = pr_review_node["createdAt"]
        last_updated_at = pr_review_node["updatedAt"]
        # label, commits, forks, stars, comments

        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name.lower(),
                "type": contribTypes.T2,
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "review_type": review_type,
                "pr_status": pr_status,
                "author_id": author_id,
                "merged_by_id": merged_by_id,
                "reactions": reactions,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )

    return df


def format_pr_contributions(
    pr_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats pull request contributions and appends them to a pandas DataFrame.

    Args:
        pr_contribution_list (List): A list of pull request contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the new contributions.
    """
    for pr in pr_contribution_list:
        github_id = pr["node"]["pullRequest"]["id"]

        pr_node = pr["node"]["pullRequest"]

        # Do not count contribution in archived repo
        if pr_node["repository"]["isArchived"]:
            continue

        repo_id = pr_node["repository"]["id"]
        repo_owner_id = pr_node["repository"]["owner"]["id"]
        pr_status = pr_node["state"]

        # Do not count contibution for closed PRs
        if pr_status == "CLOSED":
            continue
        author_id = user_id
        commits = pr_node["commits"]["totalCount"]

        merged_by_id = ""
        if pr_node["merged"] and pr_node["mergedBy"]:
            mb = pr_node["mergedBy"]
            if "id" in mb:
                merged_by_id = pr_node["mergedBy"]["id"]
        labels = []
        do_not_continue = False
        for edge in pr_node["labels"]["edges"]:
            # if invalid or spam label, do not continue
            if edge["node"]["name"] == "invalid" or edge["node"]["name"] == "spam":
                do_not_continue = True
            labels.append(edge["node"]["name"])
        label = ", ".join(labels)

        if do_not_continue:
            continue

        created_at = pr_node["createdAt"]
        last_updated_at = pr_node["updatedAt"]
        # forks, stars, comments

        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name.lower(),
                "type": contribTypes.T1,
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "pr_status": pr_status,
                "author_id": author_id,
                "label": label,
                "commits": commits,
                "merged_by_id": merged_by_id,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )

    return df


def format_issue_contributions(
    issue_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats a list of issue contributions and appends them to a pandas DataFrame.

    Args:
        issue_contribution_list (List): A list of issue contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the formatted contributions will be appended.

    Returns:
        pd.DataFrame: The pandas DataFrame with the formatted contributions appended.
    """
    for issue in issue_contribution_list:
        github_id = issue["node"]["issue"]["id"]
        issue_node = issue["node"]["issue"]
        repo_id = issue_node["repository"]["id"]
        repo_owner_id = issue_node["repository"]["owner"]["id"]
        reactions = issue_node["reactions"]["totalCount"]
        labels = []

        for edge in issue_node["labels"]["edges"]:
            labels.append(edge["node"]["name"])
        label = ", ".join(labels)

        comments = issue_node["comments"]["totalCount"]
        created_at = issue_node["createdAt"]
        last_updated_at = issue_node["updatedAt"]
        # type = 'Issue'
        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name.lower(),
                "type": contribTypes.T3,
                "repo_id": repo_id,
                "repo_owner_id": repo_owner_id,
                "reactions": reactions,
                "label": label,
                "comments": comments,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )

    return df


def format_repo_contributions(
    repo_contribution_list: List, user_id: str, user_name: str, df: pd.DataFrame
) -> pd.DataFrame:
    """
    Formats a list of repository contributions and appends them to a pandas DataFrame.

    Args:
        repo_contribution_list (List): A list of repository contributions.
        user_id (str): The ID of the user who made the contributions.
        user_name (str): The name of the user who made the contributions.
        df (pd.DataFrame): The pandas DataFrame to which the contributions will be appended.

    Returns:
        pd.DataFrame: The updated pandas DataFrame with the appended contributions.
    """
    for repo in repo_contribution_list:
        github_id = repo["node"]["repository"]["id"]
        repo_node = repo["node"]["repository"]
        repo_id = repo_node["id"]
        forks = repo_node["forkCount"]
        stars = repo_node["stargazers"]["totalCount"]
        created_at = repo_node["createdAt"]
        last_updated_at = repo_node["updatedAt"]
        is_fork = repo_node["isFork"]
        df = df.append(
            {
                "github_id": github_id,
                "user_id": user_id,
                "user_name": user_name.lower(),
                "type": contribTypes.T5,
                "repo_id": repo_id,
                "repo_owner_id": user_id,
                "forks": forks,
                "stars": stars,
                "is_fork": is_fork,
                "created_at": created_at,
                "last_updated_at": last_updated_at,
            },
            ignore_index=True,
        )

    return df
