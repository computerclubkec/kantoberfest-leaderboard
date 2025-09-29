FROM python:3.11-slim AS main

WORKDIR /app

COPY ["setup.py", "final_html_output.py", "multi_users_fetch.py", "main.py", "README.md", "./"]
COPY ["leaderboard", "./leaderboard"]
COPY ["assets", "./assets"]

RUN pip install -U -e .

CMD ["python", "main.py"]
