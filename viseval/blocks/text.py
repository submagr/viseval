from .base import Block
from dominate.util import text


class TextBlock(Block):
    def __init__(self):
        pass

    def update_doc(self, doc, data, html_root):
        for col, _, text_data in data:
            col.add(text(text_data))
        return doc
