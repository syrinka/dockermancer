from autogen_core import AgentId, SingleThreadedAgentRuntime
from loguru import logger

import core.config
import core.logging
from core.agent.chat import ChatCompletionAgent
from core.agent.dialogue import DialogueAgent
from core.agent.docker import DockerAccessAgent


async def simplechat(runtime):
    try:
        while True:
            user_msg = input("[> ")
            result = await runtime.send_message(
                user_msg,
                AgentId("dialogue", "default"),
            )
            print(f"\n{result}\n")
    except KeyboardInterrupt:
        print("Bye!")


async def main():
    logger.info("Create runtime and register all agents")
    runtime = SingleThreadedAgentRuntime()
    await runtime.register_factory("dialogue", lambda: DialogueAgent())
    await runtime.register_factory("chat", lambda: ChatCompletionAgent())
    await runtime.register_factory("docker", lambda: DockerAccessAgent())
    logger.info(f"Known agent names: {runtime._known_agent_names}")

    runtime.start()
    # await runtime.send_message(DockerRequest("asd"), AgentId("docker", "default"))
    # print(
    #     await runtime.send_message(
    #         "What is the X-Sum between 5 and 8",
    #         AgentId("dialogue", "default"),
    #     ),
    # )
    await simplechat(runtime)
    await runtime.stop_when_idle()
