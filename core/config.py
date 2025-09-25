"""Where configurations are loaded and parsed."""

import argparse
import sys
import tomllib
from pathlib import Path
from typing import Any, Literal

from loguru import logger
from pydantic import BaseModel, Field


class DockerInstConfig(BaseModel):
    url: str
    version: str = "auto"
    timeout: int | None = None
    user_agent: str | None = None
    name: str | None = None


class ChatClientConfig(BaseModel):
    provider: Literal["OpenAI", "AzureOpenAI", "AzureAI", "Ollama"]
    logging: bool = False
    params: dict[str, Any] = Field(default_factory=dict)


class DockermancerConfig(BaseModel):
    mode: Literal["dev", "prod"] = "dev"
    chat: ChatClientConfig
    dockers: list[DockerInstConfig]


parser = argparse.ArgumentParser(
    prog="Dockermancer",
    description="A tool to search, arrange and classify files",
)
parser.add_argument("-c", "--config", type=str, help="Path to config file.")
args = parser.parse_args()
logger.info(f"Boot with input arguments: {args}")


root = Path(sys.argv[0]).absolute().parent


CONFIG_FILENAME = "config.toml"

if args.config is None:
    config_path = root / CONFIG_FILENAME
else:
    config_path = Path(args.config)
logger.info(f"Using config path: {config_path}")

config_raw = tomllib.load(open(config_path, mode="rb"))
config = DockermancerConfig(**config_raw)
if config.mode == "prod" and "api_key" in config.chat.params:
    logger.warning("API key exposed")

logger.debug(f"Config loaded: \n{config.model_dump_json()}")


__all__ = ["config", "args"]
