from pathlib import PurePath
from .text import TextBlock
from .image import ImageBlock
from .mesh import MeshBlock


class BlockClassFactory:
    @staticmethod
    def get_block_cls(data):
        block_cls = None
        if isinstance(data, str):
            block_cls = TextBlock
        elif isinstance(data, PurePath):
            if data.suffix == ".png" or data.suffix == ".jpg" or data.suffix == ".gif":
                block_cls = ImageBlock
            if data.suffix == ".obj":
                block_cls = MeshBlock
        else:
            raise Exception("Unknown data type ", type(data))
        return block_cls
