from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
NAVY = "#13253D"
RED = "#B8323A"
INK = "#1C2A3A"
MUTED = "#536172"
PAPER = "#FFFFFF"
PALE = "#F3F6F9"
RULE = "#CCD4DD"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def wrap_text(draw, text, selected_font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=selected_font) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_story(draw, box, title, copy, title_size=23, body_size=18):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=8, fill=PAPER, outline=RULE, width=2)
    left = x1 + 16
    right = x2 - 16
    draw.text((left, y1 + 12), title, font=font(title_size, bold=True), fill=NAVY)
    lines = wrap_text(draw, copy, font(body_size), right - left)
    line_height = body_size + 5
    for index, line in enumerate(lines):
        draw.text(
            (left, y1 + 44 + index * line_height),
            line,
            font=font(body_size),
            fill=INK,
        )
    if y1 + 44 + len(lines) * line_height > y2 - 8:
        raise ValueError(f"Story text does not fit: {title}")


def main():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)

    draw.text((48, 38), "WORLD NEWS IN ONE IMAGE", font=font(38, bold=True), fill=NAVY)
    draw.text(
        (50, 93),
        "TUESDAY 24 NOVEMBER 2026",
        font=font(18, bold=True),
        fill=MUTED,
    )
    draw.rectangle((48, 132, 976, 138), fill=RED)

    lead_box = (48, 157, 976, 400)
    draw.rounded_rectangle(lead_box, radius=12, fill=PALE, outline=RULE, width=2)
    draw.rectangle((48, 157, 59, 465), fill=RED)
    draw.text((78, 179), "NVIDIA REINSTATES HUANG", font=font(40, bold=True), fill=NAVY)
    draw.line((78, 235, 946, 235), fill=RULE, width=2)
    lead_copy = (
        "Jensen Huang returns as Nvidia chief executive, employees cheered his return, "
        "Nvidia shares rose 31 percent on Monday, his comeback added $1tn to the company "
        "stock value, US President Donald Trump said he convinced Nvidia to reinstate "
        "him and faces backlash."
    )
    lead_lines = wrap_text(draw, lead_copy, font(22), 842)
    for index, line in enumerate(lead_lines):
        draw.text(
            (78, 258 + index * 32),
            line,
            font=font(22),
            fill=INK,
        )
    if 258 + len(lead_lines) * 32 > lead_box[3] - 12:
        raise ValueError("Lead story text does not fit")

    left = 48
    col_width = 454
    right = left + col_width + 20
    row_height = 124
    row_y = (418, 550, 682)
    draw_story(
        draw,
        (left, row_y[0], left + col_width, row_y[0] + row_height),
        "UKRAINE WAR SPREADS",
        "Ukraine sank a Russian battleship at a port in Libya.",
    )
    draw_story(
        draw,
        (right, row_y[0], right + col_width, row_y[0] + row_height),
        "SPACE THREAT",
        "NATO chief vows defence after reports Russia planned to launch a satellite "
        "carrying a nuclear warhead into space.",
    )
    draw_story(
        draw,
        (left, row_y[1], left + col_width, row_y[1] + row_height),
        "COP31 FAILS",
        "Climate talks ended without a deal, with oil producing countries, a US boycott "
        "and a dispute over finance blamed.",
    )
    draw_story(
        draw,
        (right, row_y[1], right + col_width, row_y[1] + row_height),
        "WORLD CUP 2035",
        "The UK will host the 2035 Women's World Cup, the first football World Cup in the "
        "UK since 1966.",
    )
    draw_story(
        draw,
        (left, row_y[2], 976, row_y[2] + row_height),
        "IRAN",
        "Singer Parastoo Ahmadi was flogged with 74 lashes in Qom for performing without "
        "a hijab.",
    )

    strip = (48, 824, 976, 970)
    draw.rounded_rectangle(strip, radius=8, fill=PALE, outline=RULE, width=2)
    draw.rectangle((48, 824, 976, 829), fill=RED)
    draw.text((64, 838), "ALSO TODAY", font=font(22, bold=True), fill=NAVY)
    draw.line((64, 871, 960, 871), fill=RULE, width=2)
    side_stories = (
        (
            "IOWA",
            "US Army will detonate five tonnes of expired explosives in Iowa on Wednesday.",
        ),
        (
            "AFGHAN WOMEN",
            "Afghan women with offers from UK universities say they are heartbroken after "
            "their visas were stopped.",
        ),
        (
            "DELHI AIRPORT",
            "Indian party leader Saurav Das was stopped from flying to the UK after his "
            "passport was flagged at Delhi airport.",
        ),
    )
    column_width = 288
    for index, (title, copy) in enumerate(side_stories):
        x = 64 + index * 300
        if index:
            draw.line((x - 12, 874, x - 12, 962), fill=RULE, width=1)
        draw.text((x, 874), title, font=font(16, bold=True), fill=RED)
        lines = wrap_text(draw, copy, font(16), column_width)
        for line_index, line in enumerate(lines):
            draw.text(
                (x, 894 + line_index * 17),
                line,
                font=font(16),
                fill=INK,
            )
        if 894 + len(lines) * 17 > strip[3] - 5:
            raise ValueError(f"Also-today story text does not fit: {title}")

    draw.line((48, 978, 976, 978), fill=NAVY, width=2)
    draw.text(
        (48, 985),
        "Sources: BBC News, 24 November 2026.",
        font=font(15),
        fill=MUTED,
    )
    image.save(Path(__file__).with_name("news.png"), format="PNG", optimize=True)


if __name__ == "__main__":
    main()
