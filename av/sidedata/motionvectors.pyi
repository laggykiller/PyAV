from typing import Any, Sequence

import numpy as np

from .sidedata import SideData

class MotionVectors(SideData, Sequence[Any]):
    def __getitem__(self, index: int) -> MotionVector: ...
    def __len__(self) -> int: ...
    def to_ndarray(self) -> np.ndarray[Any, Any]: ...

class MotionVector:
    source: int
    w: int
    h: int
    src_x: int
    src_y: int
    dst_x: int
    dst_y: int
    motion_x: int
    motion_y: int
    motion_scale: int
