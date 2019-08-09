from typing import Tuple


# TODO: be compatible between two modes (xyxy and xywh)
#       and switch to xyxy when possible


class Bbox:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @classmethod
    def from_coco_ann(cls, coco_ann):
        return Bbox(*coco_ann['bbox'])

    @classmethod
    def from_torch_tensor(cls, bbox):
        x_min, y_min, x_max, y_max = bbox.cpu().data.numpy().tolist()

        assert x_max >= x_min
        assert y_max >= y_min

        return Bbox(x_min, y_min, x_max - x_min, y_max - y_min)

    def discretize(self) -> "Bbox":
        return Bbox(*map(int, [self.x, self.y, self.width, self.height]))

    def corners(self) -> Tuple:
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    # def adjust(self, dc_x, dc_y, log_dw, log_dh) -> "Bbox":
    #     c_x = self.c_x + self.w * dc_x
    #     c_y = self.c_y + self.h * dc_y
    #     w = self.w * log_dw.exp()
    #     h = self.h * log_dh.exp()
    #
    #     return Bbox(c_x, c_y, w, h)