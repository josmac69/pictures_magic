import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Slider

def load_image(path):
    img = mpimg.imread(path).astype(np.float32)
    if img.max() > 1.0:
        img /= 255.0
    return img

def rgb_to_gray(img):
    if img.ndim == 2:
        gray = img
    else:
        if img.shape[2] == 4:
            img = img[..., :3]
        weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
        gray = np.dot(img, weights)
    return np.clip(gray, 0.0, 1.0)

def main():
    image_path = "../pictures/dalle1.webp"

    img = load_image(image_path)
    gray = rgb_to_gray(img)

    # Initial threshold
    t0 = 0.5
    binary = (gray >= t0).astype(np.float32)

    fig, (ax_gray, ax_bin) = plt.subplots(1, 2, figsize=(10, 4))
    plt.subplots_adjust(bottom=0.25)  # make room for slider

    ax_gray.imshow(gray, cmap="gray")
    ax_gray.set_title("Grayscale")
    ax_gray.axis("off")

    bin_im = ax_bin.imshow(binary, cmap="gray")
    ax_bin.set_title(f"Thresholded (t={t0:.2f})")
    ax_bin.axis("off")

    # Slider axis: [left, bottom, width, height] in figure coords
    ax_slider = fig.add_axes([0.2, 0.1, 0.6, 0.03])
    slider = Slider(ax_slider, "Threshold", 0.0, 1.0, valinit=t0)

    def update(val):
        t = slider.val
        new_binary = (gray >= t).astype(np.float32)
        bin_im.set_data(new_binary)
        ax_bin.set_title(f"Thresholded (t={t:.2f})")
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

if __name__ == "__main__":
    main()
