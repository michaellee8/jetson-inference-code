from typing import Generator, NewType, Any, Tuple
from utils import current_milli_time
from typing import Any, Generator
import jetson.inference
import jetson.utils
from typing import Generator, NewType, Any, Tuple, List
from consts.fixconsts import OVERLAY_FLAGS
from source.camera_input import CudaImage

DetectorOutput = Tuple[List[Tuple[Tuple[int, int, int, int], int, float]], int]

CudaImage = NewType('CudaImage', Any)

class CameraDetector(object):
    def __init__(self, vid_src, net) -> None:
        super().__init__()
        self.vid_src = vid_src
        self.net = net

    def run(self) -> Generator[Tuple[CudaImage, int], None, None]:
        
        while True:
            img: CudaImage = self.vid_src.Capture()
            detections = self.net.Detect(img, img.width, img.height, "none")
            ret: List[Tuple[Tuple[int, int, int, int], int, float]] = []
            for det in detections:
                ret.append(((det.Left, det.Top, det.Right, det.Bottom), det.ClassID, det.Confidence))
            yield (ret, current_milli_time())