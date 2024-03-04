from typing import Literal

from av.stream import Stream

class SubtitleStream(Stream):
    type: Literal["subtitle"]
