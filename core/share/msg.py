from dataclasses import dataclass, field

from autogen_core.models import SystemMessage, UserMessage
from autogen_core.tools import FunctionTool


@dataclass
class DockerRequest(object):
    prompt: str


@dataclass
class LogRequest(object):
    container: str


@dataclass
class MetricRequest(object):
    pass


@dataclass
class ChatCompletionRequest(object):
    prompt: str
    tools: list[FunctionTool] = field(default_factory=list)
