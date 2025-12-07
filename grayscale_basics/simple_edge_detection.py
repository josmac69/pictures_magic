import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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

def threshold(gray, t=0.5):
    """Return a binary image: 1 where gray >= t, else 0."""
    return (gray >= t).astype(np.float32)

def simple_edges(gray):
    """
    Very simple edge detection based on brightness gradients.
    Not as good as Sobel/Canny, but easy to implement.
    """
    # Horizontal gradient (difference between neighboring columns)
    dx = np.diff(gray, axis=1, append=gray[:, -1:])
    # Vertical gradient (difference between neighboring rows)
    dy = np.diff(gray, axis=0, append=gray[-1:, :])

    mag = np.sqrt(dx**2 + dy**2)
    if mag.max() > 0:
        mag /= mag.max()  # normalize to [0,1] for display
    return mag

def main():
    image_path = "../pictures/dalle1.webp"
    threshold_value = 0.5               # <-- tweak this

    img = load_image(image_path)
    gray = rgb_to_gray(img)
    binary = threshold(gray, threshold_value)
    edges = simple_edges(gray)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    axes[0].imshow(img)
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(gray, cmap="gray")
    axes[1].set_title("Grayscale")
    axes[1].axis("off")

    axes[2].imshow(binary, cmap="gray")
    axes[2].set_title(f"Thresholded (t={threshold_value})")
    axes[2].axis("off")

    axes[3].imshow(edges, cmap="gray")
    axes[3].set_title("Simple Edges")
    axes[3].axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
