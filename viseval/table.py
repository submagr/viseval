from typing import Dict, List
import dominate
from dominate import tags
from dominate.util import raw
from .blocks import BlockClassFactory


class Table:
    def __init__(
        self,
        table_data: List[Dict],
        col_names: List[str],
        title: str = "Visualizations",
    ):
        self.table_data = table_data
        self.col_names = col_names
        self.title = title

    @classmethod
    def from_list_dict(cls, table_data: List[Dict], title: str = "Visualizations"):
        col_names = set()
        for row_data in table_data:
            col_names.update(row_data.keys())
        col_names = sorted(list(col_names))
        return cls(table_data, col_names, title)

    def generate(self):
        # Html document
        doc = dominate.document(title=self.title)
        style = raw(
            """
            table,
            th,
            td {
                border: 1px solid black;
            }
            #my_table {
                position: absolute;
            }
        """
        )
        doc.head.add(tags.style(style))

        # Let's collect different type of blocks needed.
        # How about this API: Give me the doc and id's of the div. And their content.
        # And the doc will be updated. That's it. Yeah. Let's do this.
        block_data = {}

        with doc:  # <body>
            tags.h1(self.title)
            with tags.table(border=1, id="my_table"):  # <table>
                # Header
                with tags.tr():
                    tags.th("id")
                    for col_name in self.col_names:
                        tags.th(col_name)
                # - Rows
                for i, row_data in enumerate(self.table_data):
                    with tags.tr():
                        tags.td(i)  # id
                        for col_name in self.col_names:
                            cell_id = f"cell_{i}_{col_name}"
                            col = tags.td(id=cell_id)
                            if col_name in row_data:
                                data = row_data[col_name]
                                block_cls = BlockClassFactory.get_block_cls(data)
                                block_data[block_cls] = block_data.get(
                                    block_cls, []
                                ) + [(col, cell_id, data)]
        
        for block_cls, data in block_data.items():
            doc = block_cls().update_doc(doc, data)

        return doc.render()
