import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def load_image(path):
    """Load image from disk as float32 in [0, 1]."""
    img = mpimg.imread(path).astype(np.float32)
    if img.max() > 1.0:   # handle 0–255 images
        img /= 255.0
    return img

def rgb_to_gray(img):
    """
    Convert an RGB (or RGBA) image to grayscale using
    the luminosity method: 0.299 R + 0.587 G + 0.114 B.
    """
    # If already grayscale, just return
    if img.ndim == 2:
        return img

    # If image has alpha channel, drop it
    if img.shape[2] == 4:
        img = img[..., :3]

    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    gray = np.dot(img, weights)
    return gray

def main():
    image_path = "../pictures/dalle1.webp"  # <-- change this

    color_img = load_image(image_path)
    gray_img = rgb_to_gray(color_img)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].imshow(color_img)
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(gray_img, cmap="gray")
    axes[1].set_title("Grayscale")
    axes[1].axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
