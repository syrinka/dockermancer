from autogen_core import AgentId, MessageContext, RoutedAgent, message_handler
from autogen_core.tools import FunctionTool

from core.share import wraptool
from core.share.msg import ChatCompletionRequest


class DialogueAgent(RoutedAgent):
    tools: list[FunctionTool]

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        self.tools = [
            wraptool(self.calc_xsum),
        ]

    async def calc_xsum(self, a: int, b: int) -> int:
        "Calculate the X-Sum of two integer."
        return a + 2 * b

    @message_handler
    async def handle_dialogue(self, message: str, _: MessageContext) -> str:
        req = ChatCompletionRequest(prompt=message, tools=self.tools)
        resp = await self.send_message(req, AgentId("chat", "default"))

        return str(resp)
