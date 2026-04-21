FROM python:3.11.9-slim

RUN apt-get update && apt-get install -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# uv 설치
WORKDIR /tool
RUN curl -LO https://github.com/astral-sh/uv/releases/download/0.9.9/uv-x86_64-unknown-linux-gnu.tar.gz
RUN tar -zxvf uv-x86_64-unknown-linux-gnu.tar.gz

WORKDIR /app

COPY . .

RUN /tool/uv-x86_64-unknown-linux-gnu/uv sync

# sh 환경
RUN . .venv/bin/activate
# RUN source .venv/bin/activate

# CMD ["python", "-m", "src.main"]