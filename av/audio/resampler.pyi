from av.filter.graph import Graph

from .format import AudioFormat
from .layout import AudioLayout
from .frame import AudioFrame

class AudioResampler:
    rate: int
    frame_size: int
    format: AudioFormat
    graph: Graph | None

    def __init__(
        self,
        format: AudioFormat | None = None,
        layout: AudioLayout | None = None,
        rate: int | None = None,
        frame_size: int | None = None,
    ) -> None: ...
    def resample(self, frame: AudioFrame | None) -> list[AudioFrame]: ...
