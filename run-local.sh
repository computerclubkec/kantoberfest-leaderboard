#!/bin/bash
docker build --no-cache --target main -t kantoberfest-leaderboard .
docker run --env-file .env --mount type=bind,src="$(pwd)",target=/app kantoberfest-leaderboard
