#!/usr/bin/env python3

from pathlib import Path
from html import escape
from datetime import datetime


# ============================================================
# YOUR PROFILE CONFIGURATION
# ============================================================

USERNAME = "sumit90asa-coder"

PROFILE_INFO = [
    ("HEADER", "sumit soni"),

    ("Role", "Full Stack Developer"),
    ("Edu", "B.Sc. Information Technology · Mumbai"),
    ("Focus", "Backend Engineering · Full Stack · AI"),

    ("SECTION", "~/stack"),

    ("Lang", "Python · JavaScript · SQL"),
    ("Backend", "Django · DRF · Flask · REST APIs"),
    ("Frontend", "React · Vite · Tailwind CSS"),
    ("Data", "PostgreSQL · MySQL · Redis"),
    ("Tools", "Docker · Git · GitHub · Vercel"),

    ("SECTION", "~/projects"),

    ("SecureMail", "Privacy-first web + mobile mail platform"),
    ("CareConnect", "Healthcare and wellness technology platform"),
    ("CryptoEvo", "Interactive cryptography learning platform"),

    ("SECTION", "~/highlights"),

    ("Build", "Full-stack web and mobile product experiences"),
    ("Explore", "AI integrations · scalable APIs · open source"),

    ("SECTION", "~/reach"),

    ("GitHub", "github.com/sumit90asa-coder"),
    ("LinkedIn", "linkedin.com/in/sumit-soni-dev"),
]


# ============================================================
# SVG CONFIGURATION
# ============================================================

WIDTH = 980
HEIGHT = 620

PORTRAIT_FILE = "portrait.txt"

# Portrait position
PORTRAIT_X = 35
PORTRAIT_Y = 105

# Profile information position
INFO_X = 500
INFO_Y = 100

# Distance between label and value
VALUE_X = 600

LINE_HEIGHT = 19


# ============================================================
# COLOR THEMES
# ============================================================

THEMES = {

    "dark": {

        "background": "#0d1117",
        "header": "#161b22",
        "border": "#30363d",

        "text": "#c9d1d9",
        "muted": "#8b949e",

        "green": "#3fb950",
        "blue": "#58a6ff",
        "purple": "#bc8cff",
        "orange": "#d29922",

    },

    "light": {

        "background": "#ffffff",
        "header": "#f6f8fa",
        "border": "#d0d7de",

        "text": "#24292f",
        "muted": "#57606a",

        "green": "#1a7f37",
        "blue": "#0969da",
        "purple": "#8250df",
        "orange": "#9a6700",

    }

}


# ============================================================
# READ ASCII PORTRAIT
# ============================================================

def read_portrait():

    path = Path(__file__).parent / PORTRAIT_FILE

    if not path.exists():

        raise FileNotFoundError(

            "\nportrait.txt was not found.\n\n"
            "First run:\n"
            "python photo_to_ascii.py photo.png\n"

        )

    content = path.read_text(
        encoding="utf-8"
    )

    return content.splitlines()


# ============================================================
# SVG GENERATOR
# ============================================================

def generate_svg(theme_name):

    colors = THEMES[theme_name]

    portrait = read_portrait()

    svg = []


    # ========================================================
    # SVG START
    # ========================================================

    svg.append(

        f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<style>

    .mono {{
        font-family:
            "SFMono-Regular",
            Consolas,
            "Liberation Mono",
            Menlo,
            monospace;
    }}

    .ascii {{
        fill: {colors["purple"]};
        font-size: 7px;
    }}

    .label {{
        fill: {colors["green"]};
        font-size: 12px;
        font-weight: bold;
    }}

    .value {{
        fill: {colors["text"]};
        font-size: 12px;
    }}

    .section {{
        fill: {colors["blue"]};
        font-size: 12px;
        font-weight: bold;
    }}

    .name {{
        fill: {colors["blue"]};
        font-size: 14px;
        font-weight: bold;
    }}

    .muted {{
        fill: {colors["muted"]};
        font-size: 11px;
    }}

    .prompt {{
        fill: {colors["text"]};
        font-size: 12px;
    }}

    .cursor {{

        fill: {colors["green"]};

        animation:
            blink
            1s
            step-end
            infinite;

    }}

    @keyframes blink {{

        50% {{
            opacity: 0;
        }}

    }}

</style>
'''

    )


    # ========================================================
    # BACKGROUND
    # ========================================================

    svg.append(

        f'''
<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"

    fill="{colors["background"]}"

    stroke="{colors["border"]}"

    stroke-width="2"
/>
'''

    )


    # ========================================================
    # TERMINAL TOP BAR
    # ========================================================

    svg.append(

        f'''
<path

    d="
        M 13 1
        H {WIDTH - 13}

        A 12 12 0 0 1
        {WIDTH - 1} 13

        V 42

        H 1

        V 13

        A 12 12 0 0 1
        13 1
    "

    fill="{colors["header"]}"
/>


<line

    x1="1"

    y1="42"

    x2="{WIDTH - 1}"

    y2="42"

    stroke="{colors["border"]}"
/>
'''

    )


    # ========================================================
    # MACOS BUTTONS
    # ========================================================

    svg.append(

        '''
<circle
    cx="22"
    cy="21"
    r="6"
    fill="#ff5f56"
/>

<circle
    cx="42"
    cy="21"
    r="6"
    fill="#ffbd2e"
/>

<circle
    cx="62"
    cy="21"
    r="6"
    fill="#27c93f"
/>
'''

    )


    # ========================================================
    # TERMINAL TITLE
    # ========================================================

    svg.append(

        f'''
<text

    x="{WIDTH / 2}"

    y="26"

    text-anchor="middle"

    class="mono muted"

>

    {USERNAME} — zsh — 90×26

</text>
'''

    )


    # ========================================================
    # TOP COMMAND
    # ========================================================

    svg.append(

        f'''
<text

    x="30"

    y="72"

    class="mono prompt"

>

    <tspan

        fill="{colors["green"]}"

        font-weight="bold"

    >

        ➜

    </tspan>


    <tspan

        fill="{colors["blue"]}"

    >

        ~

    </tspan>


    <tspan>

        neofetch --profile

    </tspan>

</text>
'''

    )


    # ========================================================
    # ASCII PORTRAIT
    # ========================================================

    ascii_line_height = 8.5

    for index, line in enumerate(portrait):

        if not line.strip():
            continue

        safe_line = escape(line)

        y = (

            PORTRAIT_Y

            +

            index

            *

            ascii_line_height

        )

        svg.append(

            f'''
<text

    x="{PORTRAIT_X}"

    y="{y}"

    class="mono ascii"

    xml:space="preserve"

>

{safe_line}

</text>
'''

        )


    # ========================================================
    # PROFILE INFORMATION
    # ========================================================

    current_y = INFO_Y


    for label, value in PROFILE_INFO:


        # ----------------------------------------------------
        # PROFILE NAME
        # ----------------------------------------------------

        if label == "HEADER":

            svg.append(

                f'''
<text

    x="{INFO_X}"

    y="{current_y}"

    class="mono name"

>

{escape(value)}

</text>
'''

            )


            current_y += 15


            svg.append(

                f'''
<line

    x1="{INFO_X}"

    y1="{current_y}"

    x2="940"

    y2="{current_y}"

    stroke="{colors["border"]}"

/>
'''

            )


            current_y += 25


        # ----------------------------------------------------
        # SECTION
        # ----------------------------------------------------

        elif label == "SECTION":

            current_y += 10


            svg.append(

                f'''
<text

    x="{INFO_X}"

    y="{current_y}"

    class="mono section"

>

{escape(value)}

</text>
'''

            )


            current_y += 25


        # ----------------------------------------------------
        # NORMAL INFORMATION
        # ----------------------------------------------------

        else:

            svg.append(

                f'''
<text

    x="{INFO_X}"

    y="{current_y}"

    class="mono label"

>

{escape(label)}

</text>
'''

            )


            # Project names use orange values.
            if label in [

                "SecureMail",

                "CareConnect",

                "CryptoEvo",

            ]:

                value_color = colors["orange"]

            elif label in [

                "Focus",

                "Explore",

                "GitHub",

                "LinkedIn",

            ]:

                value_color = colors["blue"]

            else:

                value_color = colors["text"]


            svg.append(

                f'''
<text

    x="{VALUE_X}"

    y="{current_y}"

    class="mono value"

    fill="{value_color}"

>

{escape(value)}

</text>
'''

            )


            current_y += LINE_HEIGHT


    # ========================================================
    # BOTTOM TERMINAL PROMPT
    # ========================================================

    svg.append(

        f'''
<text

    x="30"

    y="590"

    class="mono prompt"

>

    <tspan

        fill="{colors["green"]}"

        font-weight="bold"

    >

        ➜

    </tspan>


    <tspan

        fill="{colors["blue"]}"

    >

        ~

    </tspan>


    <tspan>

        open to internships / collaborations

    </tspan>


    <tspan

        class="cursor"

    >

        █

    </tspan>

</text>
'''

    )


    # ========================================================
    # LAST UPDATED
    # ========================================================

    updated = datetime.now().strftime(

        "%d %b %Y"

    )


    svg.append(

        f'''
<text

    x="940"

    y="590"

    text-anchor="end"

    class="mono muted"

>

last updated {updated}

</text>
'''

    )


    # ========================================================
    # SVG END
    # ========================================================

    svg.append(

        "</svg>"

    )


    return "\n".join(svg)


# ============================================================
# GENERATE FILES
# ============================================================

def main():

    base = Path(__file__).parent


    print()

    print(
        "Reading portrait.txt..."
    )


    portrait = read_portrait()


    print(

        f"Portrait loaded: "
        f"{len(portrait)} rows"

    )


    print()


    # DARK SVG

    dark_svg = generate_svg(

        "dark"

    )


    dark_path = (

        base

        /

        "dark.svg"

    )


    dark_path.write_text(

        dark_svg,

        encoding="utf-8"

    )


    print(

        "✓ Generated dark.svg"

    )


    # LIGHT SVG

    light_svg = generate_svg(

        "light"

    )


    light_path = (

        base

        /

        "light.svg"

    )


    light_path.write_text(

        light_svg,

        encoding="utf-8"

    )


    print(

        "✓ Generated light.svg"

    )


    print()

    print(

        "Profile generation completed."

    )


    print()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    main()