#!/usr/bin/env python3
"""
gray_to_colormap.py

Apply a false-color / pseudo-color map to a grayscale image
using OpenCV's applyColorMap.

Usage:
    python gray_to_colormap.py input.jpg [--cmap JET] [--output out.png]

Colormap names (case-insensitive):
    AUTUMN, BONE, JET, WINTER, RAINBOW, OCEAN,
    SUMMER, SPRING, COOL, HSV, PINK, HOT, PARULA, MAGMA, INFERNO, PLASMA, VIRIDIS, CIVIDIS, TWILIGHT
"""

import argparse
from pathlib import Path

import cv2


COLORMAPS = {
    "AUTUMN": cv2.COLORMAP_AUTUMN,
    "BONE": cv2.COLORMAP_BONE,
    "JET": cv2.COLORMAP_JET,
    "WINTER": cv2.COLORMAP_WINTER,
    "RAINBOW": cv2.COLORMAP_RAINBOW,
    "OCEAN": cv2.COLORMAP_OCEAN,
    "SUMMER": cv2.COLORMAP_SUMMER,
    "SPRING": cv2.COLORMAP_SPRING,
    "COOL": cv2.COLORMAP_COOL,
    "HSV": cv2.COLORMAP_HSV,
    "PINK": cv2.COLORMAP_PINK,
    "HOT": cv2.COLORMAP_HOT,
    "PARULA": getattr(cv2, "COLORMAP_PARULA", cv2.COLORMAP_JET),
    "MAGMA": getattr(cv2, "COLORMAP_MAGMA", cv2.COLORMAP_JET),
    "INFERNO": getattr(cv2, "COLORMAP_INFERNO", cv2.COLORMAP_JET),
    "PLASMA": getattr(cv2, "COLORMAP_PLASMA", cv2.COLORMAP_JET),
    "VIRIDIS": getattr(cv2, "COLORMAP_VIRIDIS", cv2.COLORMAP_JET),
    "CIVIDIS": getattr(cv2, "COLORMAP_CIVIDIS", cv2.COLORMAP_JET),
    "TWILIGHT": getattr(cv2, "COLORMAP_TWILIGHT", cv2.COLORMAP_JET),
}


def apply_colormap(input_path, colormap_name="JET", output_path=None):
    """
    Apply a false-color / pseudo-color map to a grayscale image
    using OpenCV's applyColorMap.
    """
    print(f"Applying colormap '{colormap_name}' to image: {input_path}")
    input_path = Path(input_path)
    cmap_key = colormap_name.upper()
    if cmap_key not in COLORMAPS:
        raise ValueError(f"Unknown colormap '{colormap_name}'. "
                         f"Valid options: {', '.join(sorted(COLORMAPS))}")

    if output_path is None:
        suffix = f"_{cmap_key.lower()}.png"
        output_path = input_path.with_name(input_path.stem + suffix)
    else:
        output_path = Path(output_path)

    print(f"Output path: {output_path}")
    gray = cv2.imread(str(input_path), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise FileNotFoundError(f"Could not read image: {input_path}")

    # Apply color map: grayscale (H,W) → color (H,W,3)
    color = cv2.applyColorMap(gray, COLORMAPS[cmap_key])

    print(f"Saving pseudo-colored image ({cmap_key}) to: {output_path}")
    cv2.imwrite(str(output_path), color)
    print(f"Saved pseudo-colored image ({cmap_key}) to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Apply colormap to grayscale image.")
    parser.add_argument("--input", help="Path to grayscale input image")
    parser.add_argument("--cmap", default="JET", help="Colormap name (default: JET)")
    parser.add_argument("--output", help="Output image path (default: auto)")
    args = parser.parse_args()

    apply_colormap(args.input, args.cmap, args.output)


if __name__ == "__main__":
    main()
