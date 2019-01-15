import os
from .crop_img import crop_airs_dataset


DATASET_PATH = "./dataset-sample"


def test_crop_airs_dataset_creates_valid_dataset_structure():
    crop_airs_dataset(basedir=DATASET_PATH)

    new_base_dir = os.path.join(os.path.dirname(DATASET_PATH), "cropped")
    assert os.path.isdir(new_base_dir)

    new_image_dir = os.path.join(new_base_dir, "image")
    assert _is_valid_dir(new_image_dir)

    new_label_dir = os.path.join(new_base_dir, "label")
    assert _is_valid_dir(new_label_dir)

    assert _is_valid_index_txt_file(new_base_dir)


def _is_valid_index_txt_file(new_base_dir) -> bool:
    index_fname = next((file for file in os.listdir(new_base_dir) if file.endswith(".txt")))
    index_file_path = os.path.join(DATASET_PATH, index_fname)
    with open(os.path.join(new_base_dir, index_fname), "r") as new_index_file:
        new_img_fnames = {fname.strip() for fname in new_index_file}
    with open(index_file_path) as index_file:
        for img_fname in index_file:
            for idx in range(100):
                new_img_fname = img_fname.strip().replace(".tif", "") + "_%d.tif" % idx
                assert new_img_fname in new_img_fnames
    return True


def _is_valid_dir(dir_with_imgs) -> bool:
    assert os.path.isdir(dir_with_imgs)
    fnames_in_new_img_dir = os.listdir(dir_with_imgs)
    assert len(fnames_in_new_img_dir) > 0
    for fname in fnames_in_new_img_dir:
        assert fname.endswith(".tif")
    return True
