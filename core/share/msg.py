from dataclasses import dataclass, field

from autogen_core.tools import FunctionTool


@dataclass
class ChatCompletionRequest(object):
    content: str
    tools: list[FunctionTool] = field(default_factory=list)
