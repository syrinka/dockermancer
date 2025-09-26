import hashlib
from typing import Annotated

import docker
from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core.tools import FunctionTool
from docker.errors import APIError
from loguru import logger

from core.config import DockerInstConfig, config
from core.share import wraptool
from core.share.msg import ChatCompletionRequest


def get_docker_client(inst_config: DockerInstConfig) -> docker.DockerClient:
    return docker.DockerClient(**inst_config.model_dump())


class DockerAccessAgent(RoutedAgent):
    inst_config: dict[str, DockerInstConfig]
    clients: dict[str, docker.DockerClient]
    tools: list[FunctionTool]

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
        self.tools = [
            wraptool(self.get_docker_list),
            wraptool(self.ping_docker),
            wraptool(self.get_docker_info),
            wraptool(self.get_container_list),
        ]

    async def get_docker_list(self) -> list:
        """Get the list of docker instance"""
        ...

    async def ping_docker(
        self,
        inst_name: Annotated[str, "Identifier of docker instance"],
    ) -> bool:
        """Check if the server is responsive."""
        return self.clients[inst_name].ping()

    async def get_docker_info(self) -> str: ...

    async def get_container_list(self) -> list: ...

    @message_handler
    async def handle_request(self, message: str, _: MessageContext) -> str:
        try:
            req = ChatCompletionRequest(content=message, tools=self.tools)
            return await self.send_message(req, AgentId("chat", "docker"))
        except APIError:
            return "API Error"
