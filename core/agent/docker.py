import hashlib

import docker
from autogen_core import (
    MessageContext,
    RoutedAgent,
    message_handler,
)
from docker.errors import APIError
from loguru import logger

from core.config import DockerInstConfig, config
from core.share.msg import DockerRequest


def get_docker_client(inst_config: DockerInstConfig) -> docker.DockerClient:
    return docker.DockerClient(**inst_config.model_dump())


class DockerAccessAgent(RoutedAgent):
    inst_config: dict[str, DockerInstConfig]
    clients: dict[str, docker.DockerClient]

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.inst_config = dict()
        for inst in config.dockers:
            if inst.name is None:
                # Generate short hash name
                urlhash = hashlib.md5(inst.url.encode()).hexdigest()
                inst.name = "Inst-" + urlhash[:6]
                logger.info(
                    f"Gen hash name {inst.name} for instance: {inst.url}",
                )
            self.inst_config[inst.name] = inst

    @message_handler
    async def handle_request(self, message: DockerRequest, _: MessageContext) -> None:
        if message.name not in self.inst_config:
            logger.error(
                f"Try to access inexist docker instance: {message.name}",
            )
        try:
            ...
        except APIError:
            ...
