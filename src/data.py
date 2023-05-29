"""
(c) Ilya Ovodov, 2023
https://github.com/IlyaOvodov/AngelinaReader
https://github.com/IlyaOvodov/AngelinaDataset

Utlilties to read braille annotation from LabelMe json and CSV files
"""
import csv
import json
import label_tools as lt

def limiting_scaler(source, dest):
    '''
    Creates function to convert coordinates from source scale to dest with limiting to [0..dest)
    :param source: source scale
    :param dest: dest scale
    :return: function f(x) for linear conversion [0..sousce)->[0..dest) so that
        f(0) = 0, f(source-1) = (source-1)/source*dest, f(x<0)=0, f(x>=source) = (source-1)/source*dest
    '''
    def scale(x):
        return int(min(max(0, x), source-1)) * dest/source
    return scale


def read_LabelMe_annotation(label_filename):
    '''
    Reads LabelMe (see https://github.com/IlyaOvodov/labelme labelling tool) annotation JSON file.
    :param label_filename: path to LabelMe annotation JSON file
    :return: list of rect objects. Each rect object is a tuple (left, top, right, bottom, label, score) where
        left..bottom are in [0,1), label is int in [1..63]
        score is 1.0 if no 'score' key for the item. Score is set in auto-generated annotation
    '''
    with open(label_filename, 'r', encoding='cp1251') as opened_json:
        loaded = json.load(opened_json)
    convert_x = limiting_scaler(loaded["imageWidth"], 1.0)
    convert_y = limiting_scaler(loaded["imageHeight"], 1.0)
    rects = [(convert_x(min(xvals)),
              convert_y(min(yvals)),
              convert_x(max(xvals)),
              convert_y(max(yvals)),
              lt.human_label_to_int(label),
              score
              ) for label, xvals, yvals, score in
                    ((shape["label"],
                      [coords[0] for coords in shape["points"]],
                      [coords[1] for coords in shape["points"]],
                      shape.get("score", 1.0)
                     ) for shape in loaded["shapes"]
                    )
            ]
    return rects


def read_csv_annotation(label_filename):
    '''
    Reads CSV annotation with each line representing a single Braille char as:
    left;top;right;bottom;label
    :param label_filename: path to CSV annotation file
    :return: list of rect objects. Each rect object is a tuple (left, top, right, bottom, label) where
        left..bottom are in [0,1), label is int in [1..63]
    '''
    rects = []
    with open(label_filename) as f:
        csv_reader = csv.reader(f, delimiter=';')
        for left,top,right,bottom,label in csv_reader:
            rects.append((float(left), float(top), float(right), float(bottom), int(label) ))
    return rects

