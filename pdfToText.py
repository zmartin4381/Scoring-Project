
import fitz
from pathlib import Path


import subprocess
import sys
'''
meet = "Meet 2 @ Northwest Branch Pool"

input_pdf = "SwimResults/" + meet + ".pdf"
ocr_pdf = "SwimResults/" + meet + " ocr.pdf"
text_output = "TextProcessing/unprocessed.txt"
'''

pdf_file = Path(sys.argv[1])

meet_name = pdf_file.stem

input_pdf = pdf_file
ocr_pdf = Path("SwimResults") / f"{pdf_file.stem} ocr.pdf"
text_output = "TextProcessing/unprocessed.txt"


def run_ocr(input_pdf: str, output_pdf: str) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "ocrmypdf",
            "--force-ocr",
            "--oversample", "400",
            "--deskew",
            input_pdf,
            output_pdf,
        ],
        check=True,
    )



def extract_columns(
    pdf_path: str,
    output_path: str,
    meet_name: str,
    margin: float = 8,
) -> None:
    document = fitz.open(pdf_path)
    sections = []

    for page_number, page in enumerate(document, start=1):
        width = page.rect.width
        height = page.rect.height
        third = width / 3

        columns = [
            # Left column
            fitz.Rect(
                0,
                0,
                third - margin,
                height,
            ),

            # Middle column
            fitz.Rect(
                third + margin,
                0,
                (2 * third) - margin,
                height,
            ),

            # Right column
            fitz.Rect(
                (2 * third),
                0,
                width,
                height,
            ),
        ]

        for column_number, clip in enumerate(columns, start=1):
            text = page.get_text(
                "text",
                clip=clip,
                sort=True,
            )


            sections.append(
                #f"=== PAGE {page_number}, " also on next line
                #f"COLUMN {column_number} ===\n{text}"
                f"\n{text}"
            )

    Path(text_output).write_text(
    meet_name + "\n" +
    "\n\n".join(sections),
    encoding="utf-8"
)

run_ocr(input_pdf, ocr_pdf)
extract_columns(
    ocr_pdf,
    text_output,
    meet_name,
    margin=10,
)