#!/usr/bin/env python3
"""
colorize_dnn.py

Automatic grayscale image colorization using a pre-trained CNN
(Zhang et al. "Colorful Image Colorization", ECCV 2016),
via OpenCV's DNN module.

Usage:
    python colorize_dnn.py \
        --input bw_photo.jpg \
        --output bw_photo_colorized.png \
        --prototxt models/colorization_deploy_v2.prototxt \
        --model   models/colorization_release_v2.caffemodel \
        --points  models/pts_in_hull.npy
"""

import argparse
from pathlib import Path

import cv2
import numpy as np


def load_colorization_net(prototxt_path, model_path, points_path):
    """
    Load the colorization network and embed the cluster centers
    into the appropriate layers, as in the OpenCV sample.
    """
    print("[INFO] Loading colorization model...")
    net = cv2.dnn.readNetFromCaffe(str(prototxt_path), str(model_path))

    # Load cluster centers for ab channels: shape (313, 2)
    pts = np.load(str(points_path))
    # Transpose to shape (2, 313, 1, 1) as required by the network
    pts = pts.transpose().reshape(2, 313, 1, 1)

    # The network has two special layers that get these cluster centers and rebalancing
    class8_ab = net.getLayer(net.getLayerId("class8_ab"))
    conv8_313_rh = net.getLayer(net.getLayerId("conv8_313_rh"))

    class8_ab.blobs = [pts.astype("float32")]
    conv8_313_rh.blobs = [np.full((1, 313), 2.606, dtype="float32")]

    return net


def colorize_image(net, input_path, output_path=None):
    """
    Colorize a single image using the loaded network.
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_name(input_path.stem + "_colorized.png")
    else:
        output_path = Path(output_path)

    # Read the input (BGR). Even if it's B&W, OpenCV will give 3 identical channels.
    bgr = cv2.imread(str(input_path))
    if bgr is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    # Convert BGR to float32 in [0,1]
    bgr_float = bgr.astype("float32") / 255.0

    # Convert to Lab color space
    lab = cv2.cvtColor(bgr_float, cv2.COLOR_BGR2Lab)

    # Extract L channel (lightness) and resize to 224x224 for the network
    L = lab[:, :, 0]  # HxW
    H, W = L.shape

    # Network expects 224x224 L channel, mean-centered by 50
    L_resized = cv2.resize(L, (224, 224))
    L_resized -= 50  # mean-centering as in the original code/paper

    # Create input blob: shape (1,1,224,224)
    net_input = cv2.dnn.blobFromImage(L_resized)
    net.setInput(net_input)

    # Forward pass: get predicted ab values (2 channels, 224x224)
    ab_dec = net.forward()[0, :, :, :].transpose((1, 2, 0))  # 224x224x2

    # Resize ab back to original image size
    ab_dec_upscaled = cv2.resize(ab_dec, (W, H))

    # Recombine with original L channel
    lab_out = np.zeros((H, W, 3), dtype="float32")
    lab_out[:, :, 0] = L
    lab_out[:, :, 1:] = ab_dec_upscaled

    # Convert Lab → BGR
    bgr_out = cv2.cvtColor(lab_out, cv2.COLOR_Lab2BGR)

    # Clip to [0,1] then convert to uint8 [0,255]
    bgr_out = np.clip(bgr_out, 0, 1)
    bgr_out = (bgr_out * 255).astype("uint8")

    # Save result
    cv2.imwrite(str(output_path), bgr_out)
    print(f"Saved colorized image to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Automatic grayscale image colorization using a pre-trained CNN.")
    parser.add_argument("--input", required=True, help="Path to input grayscale/BW image")
    parser.add_argument("--output", help="Output path (default: <input>_colorized.png)")

    parser.add_argument("--prototxt", required=True, help="Path to colorization_deploy_v2.prototxt")
    parser.add_argument("--model", required=True, help="Path to colorization_release_v2.caffemodel")
    parser.add_argument("--points", required=True, help="Path to pts_in_hull.npy")

    args = parser.parse_args()

    net = load_colorization_net(args.prototxt, args.model, args.points)
    colorize_image(net, args.input, args.output)


if __name__ == "__main__":
    main()
