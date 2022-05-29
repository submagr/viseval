from pathlib import Path
from viseval import visualize_helper
import numpy as np
from matplotlib import pyplot as plt


def main():
    # Evaluation results directory
    eval_path = Path("eval_results")
    eval_path.mkdir(exist_ok=True)
    visualization_rows = []
    for i in range(10):
        gt_img = np.random.random((256, 256, 3))
        model_pred = np.random.random((256, 256, 3))
        visualization_row = {}

        def save_img(img, key):
            img_path = eval_path / f"{i}_{key}.png"
            plt.imsave(img_path, img)
            visualization_row[key] = img_path

        # Save gt and model predictions
        save_img(gt_img, "gt")
        save_img(model_pred, "pred")

        visualization_rows.append(visualization_row)
        plt.imsave(eval_path / f"gt_{i}.png", gt_img)
        plt.imsave(eval_path / f"pred_{i}.png", model_pred)

    # Create html visualization for images
    html_path = visualize_helper(visualization_rows, eval_path)
    print(
        f"Visualizations saved at {html_path}. Open the html file in a browser to"
        " visualize results"
    )




if __name__ == "__main__":
    main()
