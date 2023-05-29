"""
(c) Ilya Ovodov, 2023
https://github.com/IlyaOvodov/AngelinaDataset

Script to convert braille annotation from LabelMe json to CSV format
"""

from pathlib import Path
import data

def save_annotation_as_csv(annotation, fn):
    with open(fn.with_suffix(".csv"), "w") as f:
        for left, top, right, bottom, label, score in annotation:
            f.write(f"{left};{top};{right};{bottom};{label}\n")


if __name__ == "__main__":
    source_dirs = [
        "../books",
        "../handwritten",
        "../not_braille",
        "../uploaded",
    ]
    for source_dir in source_dirs:
        for fn in Path(source_dir).glob("**/*.json"):
            print("converting", fn)
            annotation = data.read_LabelMe_annotation(fn)
            save_annotation_as_csv(annotation, fn)
