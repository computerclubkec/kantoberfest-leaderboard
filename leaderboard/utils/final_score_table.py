import pandas as pd

from leaderboard.constants import scoreWeights
from leaderboard.constants import contribTypes


def get_final_score_table(
    intermediate_score_df: pd.DataFrame, user_list: list
) -> pd.DataFrame:
    """
    Returns a final score table dataframe based on the intermediate score table containing contribution counts of all sub types for given users.

    Args:
        intermediate_score_df (pandas DataFrame): Intermediate Score Table containing contribution counts of all sub types for given users.
        user_list (list): List of user names for which the final score table is to be generated.

    Returns:
        pandas DataFrame: Final score table dataframe containing the total score of each user based on their contributions across all sub types.
    """

    intermediate_score_df.set_index("user_name", inplace=True)

    final_score_table = pd.DataFrame(
        columns=[
            "User Name",
            contribTypes.T1,
            contribTypes.T2,
            contribTypes.T3,
            contribTypes.T4,
            "Total Score",
        ]
    )

    for user_name in user_list:
        t1_score, t2_score, t3_score, t4_score, total_score = (
            0,
            0,
            0,
            0,
            0,
        )

        try:
            user_row = intermediate_score_df.loc[user_name.lower()]

            t1_score = (
                user_row.t1s1 * scoreWeights.T1S1 + user_row.t1s2 * scoreWeights.T1S2
            )

            t2_score = (
                user_row.t2s1 * scoreWeights.T2S1
                + user_row.t2s2 * scoreWeights.T2S2
                + user_row.t2s3 * scoreWeights.T2S3
                + user_row.t2s4 * scoreWeights.T2S4
            )

            t3_score = (
                user_row.t3s1 * scoreWeights.T3S1 + user_row.t3s2 * scoreWeights.T3S2
            )

            t4_score = (
                user_row.t4s1 * scoreWeights.T4S1
                + user_row.t4s2 * scoreWeights.T4S2
                + user_row.t4s3 * scoreWeights.T4S3
                + user_row.t4s4 * scoreWeights.T4S4
            )

            total_score = t1_score + t2_score + t3_score + t4_score

            if total_score <= 0.0:
                continue

            final_score_table = final_score_table.append(
                {
                    "User Name": user_name,
                    contribTypes.T1: t1_score,
                    contribTypes.T2: t2_score,
                    contribTypes.T3: t3_score,
                    contribTypes.T4: t4_score,
                    "Total Score": total_score,
                },
                ignore_index=True,
            )

        except KeyError:
            if total_score <= 0.0:
                continue

            final_score_table = final_score_table.append(
                {
                    "User Name": user_name,
                    contribTypes.T1: t1_score,
                    contribTypes.T2: t2_score,
                    contribTypes.T3: t3_score,
                    contribTypes.T4: t4_score,
                    "Total Score": total_score,
                },
                ignore_index=True,
            )

    return final_score_table.sort_values(
        by=["Total Score", "User Name"], ascending=[False, True]
    )
