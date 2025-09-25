# Dockermancer

## Usage

Install [uv package manager](https://docs.astral.sh/uv/getting-started/installation/).

Build required enviroment via:

```sh
uv sync
```

Make a copy of `config.dist.toml` and rename to `config.toml`, adjust the values as needed.

Run dockermancer via:

```sh
python3 -u entry.py
```

## Log Level

| No. | Level   |
| --- | ------- |
| 5   | TRACE   |
| 6   | CHAT    |
| 8   | AUTOGEN |
| 10  | DEBUG   |
