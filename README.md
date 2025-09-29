# oss-leaderboard

OSS Leaderboard shows the top contributors based on their contribution activities on GitHub.

<img src = "https://i.imgur.com/T2dF0FX.png" width = "700">

## Usage

```bash
# Add Github Personal Access Token
# USER_LIST: users the app should track.
$ cp .env.example .env
```

> <a href="https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line" target="_blank">Get GitHub Personal Access Token</a>

#### Building

```bash
$ make run
```

## Development

#### Setting up the codebase

1. Clone the repository.

```bash
$ git clone git@github.com:leapfrogtechnology/oss-leaderboard.git

$ cd oss-leaderboard
```

2. Setup a virtualenv.

```bash
$ make venv
```

3. Activate the virtualenv.

```bash
$ source .venv/bin/activate

$ make setup
```

## Contributing

Feel free to send pull requests.
Make sure to run following commands:

```bash
$ make format
$ make check
```

## Intermediate score table

The Intermediate score table stores the counts of all the individual contribution sub-types for each of the contributors.
The labels in the table starting from T1S1 to T5S1 correspond to the following:

| Label | Contribution Subtype                                                                         |
| ----- | -------------------------------------------------------------------------------------------- |
| t1s1  | PR opened in a repo not owned by the user                                                    |
| t1s2  | PR opened in a repo owned by the user                                                        |
| t2s1  | PR reviewed that is opened by the user and contributed in the repo owned by the user         |
| t2s2  | PR reviewed that is not opened by the user and contributed in the repo owned by the user     |
| t2s3  | PR reviewed that is opened by the user and contributed in the repo not owned by the user     |
| t2s4  | PR reviewed that is not opened by the user and contributed in the repo not owned by the user |
| t3s1  | Issue created in a repo owned by the user                                                    |
| t3s2  | Issue created in a repo not owned by the user                                                |
| t4s1  | Commented on issue created by user in the repo owned by the user                             |
| t4s2  | Commented on issue not created by user in the repo owned by the user                         |
| t4s3  | Commented on issue created by user in the repo not owned by the user                         |
| t4s4  | Commented on issue not created by user in the repo not owned by the user                     |
| t5s1  | Repo created by the user                                                                     |

## License

Licensed under [The MIT License](LICENSE).
