from typing import Any, Generator
import jetson.inference
import jetson.utils
from typing import Generator, NewType, Any

CudaImage = NewType('CudaImage', Any)

class CameraInput(object):
    def __init__(self, vid_src) -> None:
        super().__init__()
        self.vid_src = vid_src

    def run(self) -> Generator[CudaImage, None, None]:
        while True:
            img: CudaImage = self.vid_src.Capture()
            yield img