from pathlib import Path
import numpy as np
from viseval.table import Table


def main():
    # Alright, let's go through all the dominate examples so that I understand
    # it's functionalties.
    from matplotlib import pyplot as plt

    def save_img(img, img_path):
        plt.imsave(str(img_path), img)
        return img_path

    eval_dir = Path("my_eval")
    eval_dir.mkdir(exist_ok=True)

    data = [
        {
            "gt_img": save_img(np.random.random((8, 8)), eval_dir / f"{i}_gt.png"),
            "pred_img": save_img(np.random.random((8, 8)), eval_dir / f"{i}_pred.png"),
            "gt_label": f"gt_label_{i}",
            "pred_label": f"pred_label_{i}",
            "gt_mesh": Path("test_three/gt.obj"),
            "pred_mesh": Path("test_three/pred.obj"),
        }
        for i in range(10)
    ]

    table = Table.from_list_dict(data)
    with open("test_new_api.html", "w") as f:
        f.write(table.generate())


if __name__ == "__main__":
    main()
