"""
(c) Ilya Ovodov, 2023
https://github.com/IlyaOvodov/AngelinaDataset

Annotation demo: display image with annotation drawn on it
"""
from pathlib import Path
import PIL
import PIL.ImageDraw
import sys
import data
import label_tools as lt

def show_anno(fn):
    if fn.suffix == ".json":
        ann = data.read_LabelMe_annotation(fn)
    else:
        ann = data.read_csv_annotation(fn.with_suffix(".csv"))
    img = PIL.Image.open(fn.with_suffix(".jpg"))
    draw = PIL.ImageDraw.Draw(img)
    for left,top,right,bottom,label in ann:
        draw.rectangle([left*img.width, top*img.height, right*img.width, bottom*img.height], outline='blue')
        draw.text((left*img.width, bottom*img.height),
                  lt.int_to_label123(label),
                  fill="black")
    img.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python annotation_demo.py <image or annotation filename>")
        fn = "../uploaded/test2/pic1617087696042.labeled.jpg"
    else:
        fn = sys.argv[1]
    show_anno(Path(fn))




