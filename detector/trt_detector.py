from typing import Any, Generator
import jetson.inference
import jetson.utils
from typing import Generator, NewType, Any, Tuple, List
from python.training.detection.ssd.code.consts.fixconsts import OVERLAY_FLAGS
from source.camera_input import CudaImage

class TrtDetector(object):
    def __init__(self, net) -> None:
        super().__init__()
        self.net = net

    # ([((box_x1, box_y1, box_x2, box_y2), labelId, probs)], timestamp)
    def run(self) -> Generator[Any, Tuple[CudaImage, int], Tuple[List[Tuple[Tuple[int, int, int, int], int, float]]], int]:
        (cuda_img, timestamp) = yield
        while True:
            detections = self.net.Detect(cuda_img, OVERLAY_FLAGS)
            ret: List[Tuple[Tuple[int, int, int, int], int, float]] = []
            for det in detections:
                ret.append(((det.Left, det.Top, det.Right, det.Bottom), det.ClassID, det.Confidence))
            (cuda_img, timestamp) = yield (ret, timestamp)
            