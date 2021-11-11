from typing import Generator, NewType, Any, Tuple
from utils import current_milli_time

CudaImage = NewType('CudaImage', Any)

class CameraInput(object):
    def __init__(self, vid_src) -> None:
        super().__init__()
        self.vid_src = vid_src

    def run(self) -> Generator[Tuple[CudaImage, int], None, None]:
        while True:
            img: CudaImage = self.vid_src.Capture()
            yield (img, current_milli_time())