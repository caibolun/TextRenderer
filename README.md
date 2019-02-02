# TextRenderer

This project is an extention of [text_renderer](https://github.com/Sanster/text_renderer). Comparing with [text_renderer](https://github.com/Sanster/text_renderer), TextRenderer supports multiple text generation for training deep learning OCR model (e.g. [caffe_ocr](https://github.com/senlinuc/caffe_ocr)):

- Suport color image generation

- Sohu news corpus generation

- ID Card number generation
 
- ID Card name generation
 
- Label file (`labels.txt`) generation for [caffe_ocr](https://github.com/senlinuc/caffe_ocr)

## Setup
Install dependencies:
```
pip install -r requirements.txt
```

## Demo
### 1. For general OCR
By default, simply run `sh generate_default.py` and generate 20 text images
and a `labels.txt` file in `output/default/`.

![example1.jpg](./imgs/example1.jpg)
![example2.jpg](./imgs/example2.jpg)

![example3.jpg](./imgs/example3.jpg)
![example4.jpg](./imgs/example4.jpg)

### 2. For ID card number OCR
For ID card number OCR, simply run `sh generate_cardid.sh` and generate 20 text images
and a `labels.txt` file in `output/cardid/`.

![cardid1.jpg](./output/cardid/00000000.jpg)
![cardid2.jpg](./output/cardid/00000001.jpg)

![cardid3.jpg](./output/cardid/00000002.jpg)
![cardid4.jpg](./output/cardid/00000003.jpg)

### 3. For ID card name OCR
For ID card name OCR, simply run `sh generate_name.sh` and generate 20 text images
and a `labels.txt` file in `output/name/`.

![name1.jpg](./output/name/00000000.jpg)
![name2.jpg](./output/name/00000001.jpg)

![name3.jpg](./output/name/00000002.jpg)
![name4.jpg](./output/name/00000003.jpg)

### 3. For Sohu news corpus OCR
For Sohu news corpus, simply run `sh generate_sohu.sh` and generate 20 text images
and a `labels.txt` file in `output/sohu/`.

![sohu1.jpg](./output/sohu/00000002.jpg)
![sohu2.jpg](./output/sohu/00000001.jpg)

![sohu3.jpg](./output/sohu/00000003.jpg)
![sohu4.jpg](./output/sohu/00000004.jpg)

## Config
1. Please run `python main.py --help` to see all optional arguments and their meanings.
And put your own data in corresponding folder.

2. Config text effects and fraction in `configs/default.yaml`, `configs/cardid.yaml`, `configs/name.yaml` file (or create a new config file and use it by `--config_file` option):

|Effect name|Image|
|------------|----|
|Origin(Font size 25)|![origin](./imgs/effects/origin.jpg)|
|Perspective Transform|![perspective](./imgs/effects/perspective_transform.jpg)|
|Light border|![light border](./imgs/effects/light_border.jpg)|
|Dark border|![dark border](./imgs/effects/dark_border.jpg)|
|Random char space big|![random char space big](./imgs/effects/random_space_big.jpg)|
|Random char space small|![random char space small](./imgs/effects/random_space_small.jpg)|
|Reverse color|![reverse color](./imgs/effects/reverse.jpg)|
|Blur|![blur](./imgs/effects/blur.jpg)|
|Font size(15)|![font size 15](./imgs/effects/font_size_15.jpg)|
|Font size(40)|![font size 40](./imgs/effects/font_size_40.jpg)|
|Middle line|![middle line](./imgs/effects/line_middle.jpg)|
|Table line|![table line](./imgs/effects/line_table.jpg)|
|Under line|![under line](./imgs/effects/line_under.jpg)|

## Generate image using GPU
If you want to use GPU to make generate image faster, first compile opencv with CUDA.
[Compiling OpenCV with CUDA support](https://www.pyimagesearch.com/2016/07/11/compiling-opencv-with-cuda-support/)

Then build Cython part, and add `--gpu` option when run `main.py`
```
cd libs/gpu
python setup.py build_ext --inplace
```

## Concat

Please contact <arlencai@tencent.com>
