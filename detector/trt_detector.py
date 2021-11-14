from typing import Any, Generator
import jetson.inference
import jetson.utils
from typing import Generator, NewType, Any, Tuple, List
from consts.fixconsts import OVERLAY_FLAGS
from source.camera_input import CudaImage

DetectorOutput = Tuple[List[Tuple[Tuple[int, int, int, int], int, float]], int]

class TrtDetector(object):
    def __init__(self, net) -> None:
        super().__init__()
        self.net = net

    # ([((box_x1, box_y1, box_x2, box_y2), labelId, probs)], timestamp)
    def run(self) -> Generator[Tuple[List[Tuple[Tuple[int, int, int, int], int, float]], int], Tuple[CudaImage, int], None]:
        (cuda_img, timestamp) = yield
        print("cudaimg", cuda_img)
        while True:
            detections = self.net.Detect(cuda_img, overlay="none")
            ret: List[Tuple[Tuple[int, int, int, int], int, float]] = []
            for det in detections:
                ret.append(((det.Left, det.Top, det.Right, det.Bottom), det.ClassID, det.Confidence))
            (cuda_img, timestamp) = yield (ret, timestamp)
            