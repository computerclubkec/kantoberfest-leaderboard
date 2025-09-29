""" GraphQL Query to fetch data. """

query = """
query ossQuery($timedelta: DateTime!, $username: String!, $dataCount: Int!, $issueCommentDataCount: Int!, $pullReqCursor: String, $pullreqreviewcursor: String, $issueCursor: String , $issueCommentsCursor: String, $repoCursor: String) {
  user(login: $username) {
    username: login
    id
    issueComments(last: $issueCommentDataCount before:$issueCommentsCursor) {
      totalCount
      pageInfo {
        hasPreviousPage
        startCursor
      }
      edges {
        cursor
        node {
          issue {
            author {
              login
              ... on User {
                id
              }
            }
            repository {
              id
              isArchived
              owner {
                id
              }
            }
            reactions {
              totalCount
            }
          }
          id
          createdAt
          updatedAt
        }
      }
    }
    contributionsCollection(from: $timedelta) {
      hasAnyContributions
      pullRequestReviewContributions(first: $dataCount after:$pullreqreviewcursor) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          cursor
          node {
            repository {
              id
              name
              isArchived
              owner {
                id
                login
              }
            }
            pullRequestReview {
              ReviewState: state
              pullRequest {
                id
                author {
                  login
                  ... on User {
                    id
                  }
                }
                url
                state
                merged
                mergedBy {
                  login
                }
              }
              reactions {
                totalCount
              }
              id
              createdAt
              updatedAt
            }
          }
        }
      }
      issueContributions(first: $dataCount after:$issueCursor) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          cursor
          node {
            issue {
              repository {
                id
                isArchived
                owner {
                  id
                }
              }
              reactions {
                totalCount
              }
              labels(first: $dataCount) {
                edges {
                  node {
                    name
                  }
                }
              }
              url
              comments {
                totalCount
              }
              state
              closed
              id
              createdAt
              updatedAt
            }
          }
        }
      }
      pullRequestContributions(first: $dataCount after:$pullReqCursor) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          node {
            pullRequest {
              repository {
                id
                isArchived
                owner {
                  id
                }
              }
              state
              title
              closed
              merged
              mergedAt
              mergedBy {
                login
                ... on User {
                  id
                }
              }
              labels(first: $dataCount) {
                edges {
                  node {
                    name
                  }
                }
              }
              commits {
                totalCount
              }
              id
              createdAt
              updatedAt
            }
          }
        }
      }
      repositoryContributions(first: $dataCount after:$repoCursor) {
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          node {
            repository {
              id
              name
              isFork
              isArchived
              parent {
                id
                owner {
                  id
                  login
                }
              }
              isTemplate
              isFork
              isArchived
              isDisabled
              forkCount
              stargazers {
                totalCount
              }
              createdAt
              updatedAt
            }
          }
        }
      }
    }
  }
}
"""
