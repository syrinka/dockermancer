import asyncio
import json

from autogen_core import (
    CancellationToken,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    FunctionExecutionResult,
    FunctionExecutionResultMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import FunctionTool
from autogen_ext.models.openai import OpenAIChatCompletionClient

from core.config import config
from core.share.msg import ChatCompletionRequest


class ChatCompletionAgent(RoutedAgent):
    client: ChatCompletionClient
    context: BufferedChatCompletionContext
    system_prompt: list[SystemMessage]

    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)
        chat_config = config.chat
        match chat_config.provider:
            case "OpenAI":
                self.client = OpenAIChatCompletionClient(**chat_config.params)
            case _:
                raise NotImplementedError("Not yet support")
        self.context = BufferedChatCompletionContext(buffer_size=8)
        self.system_prompt = [SystemMessage(content="</System Prompt End>")]

    @message_handler
    async def handle_request(
        self,
        message: ChatCompletionRequest,
        ctx: MessageContext,
    ) -> str:
        user_msg = UserMessage(content=message.prompt, source="user")
        await self.context.add_message(user_msg)

        while True:
            result = await self.client.create(
                self.system_prompt + await self.context.get_messages(),
                tools=message.tools,
                cancellation_token=ctx.cancellation_token,
            )

            await self.context.add_message(
                AssistantMessage(content=result.content, source="assistant"),
            )

            # If not function call just return
            if result.finish_reason != "function_calls":
                assert isinstance(result.content, str)
                return result.content
            assert isinstance(result.content, list) and all(
                isinstance(item, FunctionCall) for item in result.content
            )

            executes = await asyncio.gather(
                *[
                    self.execute_tool_call(call, message.tools, ctx.cancellation_token)
                    for call in result.content
                ],
            )

            await self.context.add_message(
                FunctionExecutionResultMessage(content=executes),
            )

    async def execute_tool_call(
        self,
        call: FunctionCall,
        tools: list[FunctionTool],
        cancellation_token: CancellationToken,
    ) -> FunctionExecutionResult:
        # https://msdocs.cn/autogen/stable/user-guide/core-user-guide/components/tools.html#tool-equipped-agent
        # Find the tool by name.
        tool = next((tool for tool in tools if tool.name == call.name), None)
        assert tool is not None

        # Run the tool and capture the result.
        try:
            arguments = json.loads(call.arguments)
            result = await tool.run_json(arguments, cancellation_token)
            return FunctionExecutionResult(
                call_id=call.id,
                content=tool.return_value_as_string(result),
                is_error=False,
                name=tool.name,
            )
        except Exception as e:
            return FunctionExecutionResult(
                call_id=call.id,
                content=str(e),
                is_error=True,
                name=tool.name,
            )
