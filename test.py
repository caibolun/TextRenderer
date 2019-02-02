#!/usr/env/bin python3

"""
Generate training and test images.
"""
import traceback
import numpy as np

import multiprocessing as mp
from itertools import repeat
import os

import cv2

from libs.config import load_config
from libs.timer import Timer
from parse_args import parse_args
import libs.utils as utils
import libs.font_utils as font_utils
from textrenderer.corpus import RandomCorpus, ChnCorpus, EngCorpus, IdCorpus, NameCorpus, SohuCorpus
from textrenderer.renderer import Renderer
from tenacity import retry

lock = mp.Lock()
counter = mp.Value('i', 0)
STOP_TOKEN = 'kill'

corpus_classes = {
    "random": RandomCorpus,
    "chn": ChnCorpus,
    "eng": EngCorpus,
    "cardid": IdCorpus,
    "name": NameCorpus,
    "sohu": SohuCorpus
}

flags = parse_args()
cfg = load_config(flags.config_file)

fonts = font_utils.get_font_paths(flags.fonts_dir)
bgs = utils.load_bgs(flags.bg_dir)

corpus_class = corpus_classes[flags.corpus_mode]

if flags.length == 10 and flags.corpus_mode == 'eng':
    flags.length = 3
if  flags.corpus_mode == 'cardid':
    flags.length = 18
if  flags.corpus_mode == 'name':
    flags.length = 10
if  flags.corpus_mode == 'sohu':
    flags.length = 12
corpus = corpus_class(chars_file=flags.chars_file, corpus_dir=flags.corpus_dir, length=flags.length)

renderer = Renderer(corpus, fonts, bgs, cfg,
                    height=flags.img_height,
                    width=flags.img_width,
                    clip_max_chars=flags.clip_max_chars,
                    debug=flags.debug,
                    gpu=flags.gpu,
                    strict=flags.strict)


im, word = renderer.gen_img()
cv2.imshow("img", np.uint8(im))
cv2.waitKey(0)