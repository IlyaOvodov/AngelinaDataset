# Angelina Braille Images Dataset

<div align=center><img width="40%" src="pics/raw.jpg?raw=true"/>&nbsp;&nbsp;<img width="40%" src="pics/labeled.jpg?raw=true"/></div> 

## Dataset description

This dataset contains labeled photos of Braille texts.

It includes 
- 212 pages of two-sided printed Braille books 
- 28 handwritten student works
- 44 non-braille photos of various documents found in Internet (as auxiliary negative examples)
- 50 extra pages (printed Braille books and handwritten student works) as a test set (added in v.1.1) 

Each group of images has a predefined partition into train, validation and test sets. Appropriate image lists are stored in `train.txt`, `val.txt` and `test.txt` files in corresponding directories:

| folder  | train | val | test | total images count |
| ----- | :---: | :---: | ---: | ---: |
| books | 169 | 43 | | 212 |
| handwritten | 22 | 6 | | 28 |
| not braille | 44 | | | 44 |
| uploaded |   | | 50 | 50 |

The last group "uploaded" was added in version 1.1 and contains 50 randomly selected imaged, uploaded by users of the [Angelina Braille Reader](https://angelina-reader.ru/) Braille recognition service. So in should be considered as a more relevant test set than subsets of the two former groups.

## Dataset structure

Each group of images is located in separate folder that contains  `*.txt` files with image file lists and image and annotation files in its sub-folders.

Each line in a list `*.txt` file is a path to image `<image filename>.jpg`  file, relative to the `*.txt` file folder.

Image annotations are provided in two formats: CSV and [LabelMe](https://github.com/wkentaro/labelme) JSON. The two formats are 
provided for convenience and contain similar information. Primarily the annotation was produced using [LabelMe](https://github.com/wkentaro/labelme) tool and than converted to CSV using script (see below).

Each image file `<image filename>.jpg` has two files `<image filename>.csv` and `<image filename>.json`  next to it, with CSV and LabelMe annotations respectively. For two-side pages only front side is labeled.

## Annotation format

### CSV annotation

Each row represents bounding box and letter of one Braille character as:
`<left>;<top>;<right>;<bottom>;<label>`.

`<left>;<top>;<right>;<bottom>` are the box coordinates scaled to range [0,1], so that point (0,0) correspondes to the left top corner of an image and (1,1) is the bottom right point of an image.

`<label>` is an integer in range `[1,63] ` denoting Braille dots that present in a symbol. Each of the 6 Braille dots is encoded by a bit in the binary notation of the number. The 1st dot corresponds to the lowest bit, the 6th dot - to the highest bit.

<div align=center><img width="40%" src="pics/encoding.jpg?raw=true"/></div>

Reading function for this dataset is implemented in [read_csv_annotation](https://github.com/IlyaOvodov/AngelinaDataset/blob/e5d86078982b750b7624a681ab2fed5f04b40eb8/src/data.py#LL54C8-L54C8) function.


### LabelMe annotation

Label files for [LabelMe](https://github.com/wkentaro/labelme) annotation tool has a JSON format.

Each Braille symbol is labeled as 
* corresponding plain text letter or symbol (mainly Russian letter)
* '\~_number_' or '\~_number_\~' where _number_ is a digital representation of the Braille symbol (for example '\~3456' for digital sign)
* some special marks like '##' for digital sign

Correspondence between Braille symbols and correspondent letters is defined at [letters.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/letters.py) file.

Some special symbols can be labeled in several ways. See [labeling_synonyms](https://github.com/IlyaOvodov/AngelinaDataset/blob/e5d86078982b750b7624a681ab2fed5f04b40eb8/src/label_tools.py#L93) dict.

Various tools for handling labels can be found at [label_tools.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/label_tools.py) file.

Reading function for this dataset is implemented in [read_LabelMe_annotation](https://github.com/IlyaOvodov/AngelinaDataset/blob/e5d86078982b750b7624a681ab2fed5f04b40eb8/src/data.py#L25) function.

Implementation of PyTorch Dataset is [here](https://github.com/IlyaOvodov/AngelinaReader/blob/328b0e0d30353d76ec06cde8560a876da5c46ab7/data_utils/data.py#L171).         

## Tools

Some scripts for handling this dataset can are provided in `src` folder.
- File [letters.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/letters.py): dicts with letters, numbers and special chars corresponding Braille symbols in English and Russian;
- File [label_tools.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/label_tools.py): functions to convert between different representations of Braille symbol:

| representations name | encoding for A symbol | encoding for B symbol | encoding for C symbol | encoding for all braille dots used |
| --- | --- | --- | --- | ---- |
| int encoding | 1 | 3| 9 | 63 |
| 123 encoding | 1 | 12 | 14 | 123456 |
| 010 encoding | 100000 | 110000 | 100100 | 111111 |
| unicode | ⠁| ⠃ | ⠉ | ⠿ |
| ascii | A | B | C | = |

- [data.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/data.py): functions to read CSV and JSON annotation files
- [convert_json_to_csv.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/convert_json_to_csv.py): script to convert JSON annotation to CSV
- [annotation_demo.py](https://github.com/IlyaOvodov/AngelinaDataset/blob/master/src/annotation_demo.py): script to draw annotations on image for demo and debug purposes.

More tools for handling this dataset can be found at [Angelina Braille Reader](https://github.com/IlyaOvodov/AngelinaReader) repository.

## Update history
- 26.11.2020 - release 1.0.
- 29.05.2023 - release 1.1. Test set of 50 random user images added.  CSV annotation format and annotation handling scripts added.


# Citation

Ovodov, Ilya G. _"Optical Braille Recognition Using Object Detection Neural Network."_ Proceedings of the IEEE/CVF International Conference on Computer Vision. 2021.

```
@inproceedings{ovodov2021optical,
  title={Optical Braille Recognition Using Object Detection Neural Network},
  author={Ovodov, Ilya G},
  booktitle={Proceedings of the IEEE/CVF International Conference on Computer Vision},
  pages={1741--1748},
  year={2021}
}
```