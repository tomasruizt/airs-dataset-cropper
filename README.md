## Requirements
```bash
python -m pip install -r requirements.txt
```
## Example
if the directory with `image` and `label` is `./dataset-sample`:
```bash
python crop_img.py --dataset-dir=./dataset-sample --processes=2
```

Detached example:
```bash
python crop_img.py --dataset-dir=./dataset-sample --processes=10 &>out.log &
```

## Testing
```bash
python -m pytest
```