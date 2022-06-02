from .base import Block
from dominate import tags


class ImageBlock(Block):
    def __init__(self):
        pass

    def update_doc(self, doc, data, html_root):
        for col, _, img_path in data:
            col.add(
                tags.img(
                    style="height: 128px", src=str(img_path.relative_to(html_root))
                )
            )
        return doc
