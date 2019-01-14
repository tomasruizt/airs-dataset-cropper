import os
from argparse import ArgumentParser

from itertools import product, repeat
from PIL import Image
import numpy as np
from multiprocessing.pool import Pool

Image.MAX_IMAGE_PIXELS = None


def crop_airs_dataset(basedir: str, processes: int = 4) -> None:
    """
    Crops the imgs of the airs dataset by 10 in each direction and puts
    all new images into a new folder called 'cropped' besides the input
    'basedir'. The new numbering of imgs adds a suffix to the original
    numbering and goes from left to right and top to botton through the
    cropped parts of the original img.
    :param basedir: The directory containing a "image" and "label" dir.
    :param processes: Number of parallel processes performing cropping.
    :return: None
    """
    assert os.path.isdir(basedir)
    image_dir = os.path.join(basedir, "image")
    assert os.path.isdir(image_dir)
    label_dir = os.path.join(basedir, "label")
    assert os.path.isdir(label_dir)
    train_txt_file = os.path.join(basedir, "train.txt")
    assert os.path.exists(train_txt_file)

    new_basedir = os.path.join(os.path.dirname(basedir), "cropped")

    for suffix in ["image", "label"]:
        new_dir = os.path.join(new_basedir, suffix)
        os.makedirs(new_dir, exist_ok=True)
        img_dir = os.path.join(basedir, suffix)
        img_paths = (os.path.join(img_dir, fname) for fname in os.listdir(img_dir))
        with Pool(processes=processes) as p:
            p.map(_wrapper_crop_100_imgs_and_dump, zip(img_paths, repeat(new_dir)))

    new_train_txt_file = os.path.join(new_basedir, "train.txt")
    with open(train_txt_file, "r") as file, open(new_train_txt_file, "a") as out_file:
        for img_fname in file:
            for idx in range(100):
                new_fname = img_fname.strip().replace(".tif", "") + "_%d.tif" % idx
                out_file.write(new_fname + "\n")


def _wrapper_crop_100_imgs_and_dump(img_and_dir):
    img_path, output_dir = img_and_dir
    _crop_into_100_imgs_and_dump(img_path, output_dir)


def _crop_into_100_imgs_and_dump(source_img_path: str, output_dir: str):
    source_img = Image.open(source_img_path)
    space = np.linspace(0, 9000, 10)

    cropped_img_size = source_img.size[0] / 10
    for idx, corner_coordinates in enumerate(product(space, space)):
        cropped_img_fname = os.path.basename(source_img_path).replace(".tif", "") + "_%d.tif" % idx
        cropped_img_full_path = os.path.join(output_dir, cropped_img_fname)
        if os.path.exists(cropped_img_full_path):
            continue
        x, y = corner_coordinates
        cropped_img = source_img.crop((y, x, y + cropped_img_size, x + cropped_img_size))
        cropped_img.save(cropped_img_full_path)
    print("cropped img {}".format(source_img_path))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--dataset-dir")
    parser.add_argument("--processes", nargs="?", default=4)
    args = parser.parse_args()
    crop_airs_dataset(basedir=args.dataset_dir, processes=int(args.processes))
