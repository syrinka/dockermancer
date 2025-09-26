from dataclasses import dataclass, field

from autogen_core.models import SystemMessage, UserMessage
from autogen_core.tools import FunctionTool


@dataclass
class ChatCompletionRequest(object):
    prompt: str
    tools: list[FunctionTool] = field(default_factory=list)
