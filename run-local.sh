#!/bin/bash

docker build --no-cache --target main -t oss-leaderboard .
docker run --env-file .env --mount type=bind,src="$(pwd)",target=/app oss-leaderboard
