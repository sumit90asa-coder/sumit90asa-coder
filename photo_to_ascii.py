#!/usr/bin/env python3

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import remove


# ============================================================
# CONFIGURATION
# ============================================================

SRC = sys.argv[1] if len(sys.argv) > 1 else "photo.png"

# 70–80 gives a detailed portrait without making it too wide.
COLS = 76

# Compensates for monospace character proportions.
ASPECT = 1.90

# Keep only head, shoulders and a little upper body.
BUST = 0.56

# Image-detail settings.
DETAIL = 2.8
WEIGHT = 0.55

# Darkest -> lightest.
RAMP = "@%#*+=-:. "


# ============================================================
# IMAGE → ASCII
# ============================================================

def main():

    print(f"Loading: {SRC}")

    image = Image.open(SRC).convert("RGBA")

    # --------------------------------------------------------
    # 1. REMOVE BACKGROUND
    # --------------------------------------------------------

    cut = remove(
        image,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=10,
        alpha_matting_erode_size=8,
    )

    rgba = np.asarray(cut)
    alpha = rgba[:, :, 3]

    # Detect actual subject.
    ys, xs = np.nonzero(alpha > 35)

    if len(xs) == 0:
        raise RuntimeError(
            "No person detected after background removal."
        )

    # --------------------------------------------------------
    # 2. GET PERSON BOUNDING BOX
    # --------------------------------------------------------

    x0 = xs.min()
    x1 = xs.max()

    y0 = ys.min()
    subject_bottom = ys.max()

    subject_height = subject_bottom - y0

    # Keep only upper body.
    y1 = int(
        y0 +
        subject_height * BUST
    )

    subject_width = x1 - x0

    # Small horizontal padding.
    x_padding = int(subject_width * 0.05)

    # Small top padding.
    top_padding = int(subject_height * 0.02)

    box = (

        max(
            0,
            x0 - x_padding
        ),

        max(
            0,
            y0 - top_padding
        ),

        min(
            rgba.shape[1],
            x1 + x_padding
        ),

        min(
            rgba.shape[0],
            y1
        )

    )

    cut = cut.crop(box)

    # --------------------------------------------------------
    # 3. GET ALPHA MASK
    # --------------------------------------------------------

    rgba = np.asarray(cut)

    alpha = (
        rgba[:, :, 3]
        .astype(np.float32)
        / 255
    )

    # --------------------------------------------------------
    # 4. GRAYSCALE IMAGE
    # --------------------------------------------------------

    gray_image = ImageOps.autocontrast(
        cut.convert("L"),
        cutoff=1
    )

    gray = np.asarray(
        gray_image,
        dtype=np.float32
    )

    height, width = gray.shape

    # --------------------------------------------------------
    # 5. LOCAL CONTRAST
    #
    # Makes:
    # - face visible
    # - hair visible
    # - jacket folds visible
    # - white shirt separated
    # --------------------------------------------------------

    blur_radius = max(
        2,
        width // 50
    )

    blurred = np.asarray(

        Image
        .fromarray(
            gray.astype(np.uint8)
        )
        .filter(
            ImageFilter.GaussianBlur(
                blur_radius
            )
        ),

        dtype=np.float32

    )

    local_detail = (
        gray -
        blurred
    )

    ink = (

        145 +

        local_detail * DETAIL +

        (gray - 128) * WEIGHT

    )

    ink = np.clip(
        ink,
        0,
        255
    )

    # --------------------------------------------------------
    # 6. NORMALIZE ONLY PERSON PIXELS
    # --------------------------------------------------------

    inside = alpha > 0.40

    if inside.any():

        values = ink[inside]

        low = np.percentile(
            values,
            1
        )

        high = np.percentile(
            values,
            99
        )

        ink = (

            (ink - low)

            * 255

            / max(
                1,
                high - low
            )

        )

        ink = np.clip(
            ink,
            0,
            255
        )

    # --------------------------------------------------------
    # 7. CALCULATE ASCII SIZE
    # --------------------------------------------------------

    rows = max(

        1,

        int(

            COLS

            * (
                height /
                width
            )

            / ASPECT

        )

    )

    # --------------------------------------------------------
    # 8. RESIZE IMAGE
    # --------------------------------------------------------

    ascii_image = (

        Image
        .fromarray(
            ink.astype(np.uint8)
        )
        .resize(

            (
                COLS,
                rows
            ),

            Image.Resampling.LANCZOS

        )

    )

    ascii_pixels = np.asarray(
        ascii_image,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # 9. RESIZE MASK
    # --------------------------------------------------------

    mask_image = (

        Image
        .fromarray(

            (
                alpha *
                255
            )
            .astype(
                np.uint8
            )

        )
        .resize(

            (
                COLS,
                rows
            ),

            Image.Resampling.LANCZOS

        )

    )

    mask = np.asarray(
        mask_image,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # 10. CREATE ASCII
    # --------------------------------------------------------

    ramp_size = (
        len(RAMP) - 1
    )

    lines = []

    for y in range(rows):

        characters = []

        for x in range(COLS):

            # Transparent background.
            if mask[y, x] < 80:

                characters.append(
                    " "
                )

                continue

            value = (
                ascii_pixels[y, x]
                / 255
            )

            index = round(

                value *
                ramp_size

            )

            index = max(

                0,

                min(
                    ramp_size,
                    index
                )

            )

            characters.append(
                RAMP[index]
            )

        line = "".join(
            characters
        )

        lines.append(
            line.rstrip()
        )

    # --------------------------------------------------------
    # 11. REMOVE EMPTY TOP/BOTTOM ROWS
    # --------------------------------------------------------

    while (
        lines and
        not lines[0].strip()
    ):

        lines.pop(0)

    while (
        lines and
        not lines[-1].strip()
    ):

        lines.pop()

    # --------------------------------------------------------
    # 12. CENTER PORTRAIT
    # --------------------------------------------------------

    visible_width = max(

        len(line)

        for line in lines

    )

    centered_lines = []

    for line in lines:

        left_space = (

            COLS -
            visible_width

        ) // 2

        centered_lines.append(

            " " *
            left_space +

            line

        )

    # --------------------------------------------------------
    # 13. SAVE portrait.txt
    # --------------------------------------------------------

    output = (

        Path(__file__)
        .parent
        / "portrait.txt"

    )

    output.write_text(

        "\n".join(
            centered_lines
        ),

        encoding="utf-8"

    )

    print()
    print(
        "\n".join(
            centered_lines
        )
    )

    print()

    print(
        f"Generated portrait.txt "
        f"({COLS} columns × "
        f"{len(centered_lines)} rows)"
    )


if __name__ == "__main__":

    main()