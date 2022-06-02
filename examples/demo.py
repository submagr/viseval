from pathlib import Path
import numpy as np
from viseval import Table
from matplotlib import pyplot as plt
from shutil import copy


def main():
    eval_dir = Path("eval_results")
    eval_dir.mkdir(exist_ok=True)

    def save_img(img, img_path):
        plt.imsave(img_path, img)
        return img_path

    # Genearate dummy data for demonstration
    gt_mesh_path = eval_dir / "gt.obj"
    copy("resources/gt.obj", gt_mesh_path)
    pred_mesh_path = eval_dir / "pred.obj"
    copy("resources/pred.obj", pred_mesh_path)
    vis_data = []
    for i in range(10):
        vis_data.append(
            {
                "gt_img": save_img(np.random.random((8, 8)), eval_dir / f"{i}_gt.png"),
                "pred_img": save_img(
                    np.random.random((8, 8)), eval_dir / f"{i}_pred.png"
                ),
                "gt_label": f"gt_label_{i}",
                "pred_label": f"pred_label_{i}",
                "gt_mesh": gt_mesh_path,
                "pred_mesh": pred_mesh_path,
            }
        )

    table = Table.from_list_dict(vis_data, eval_dir)
    html_path = table.generate()
    print(
        f"Visualizations saved at {html_path}. Use python -m http.server from inside {html_path.parent} directory to visualize the html"
    )


if __name__ == "__main__":
    main()
