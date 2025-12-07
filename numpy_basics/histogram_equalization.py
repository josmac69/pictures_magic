import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def load_image(path):
    img = mpimg.imread(path).astype(np.float32)
    if img.max() > 1.0:
        img /= 255.0
    if img.ndim == 2:
        # expand grayscale to "fake RGB"
        img = np.stack([img, img, img], axis=-1)
    if img.shape[2] == 4:
        img = img[..., :3]
    return img

def gray_average(img):
    return img.mean(axis=2)

def gray_lightness(img):
    max_rgb = img.max(axis=2)
    min_rgb = img.min(axis=2)
    return (max_rgb + min_rgb) / 2.0

def gray_luminosity(img):
    weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    return np.dot(img, weights)

def main():
    image_path = "../pictures/dalle1.webp"
    img = load_image(image_path)

    g_avg = gray_average(img)
    g_lightness = gray_lightness(img)
    g_lum = gray_luminosity(img)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))

    axes[0].imshow(img)
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(g_avg, cmap="gray")
    axes[1].set_title("Average")
    axes[1].axis("off")

    axes[2].imshow(g_lightness, cmap="gray")
    axes[2].set_title("Lightness")
    axes[2].axis("off")

    axes[3].imshow(g_lum, cmap="gray")
    axes[3].set_title("Luminosity")
    axes[3].axis("off")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
