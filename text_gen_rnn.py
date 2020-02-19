# created with the TensorFlow tutorial at: https://www.tensorflow.org/tutorials/text/text_generation

from __future__ import absolute_import, division, print_function, unicode_literals

import tensorflow as tf

import numpy as np
import os
import time

# Read, then decode for py2 compat.
text = open('data/Irene Iddesleigh clean.txt', 'rb').read().decode(encoding='utf-8')
# length of text is the number of characters in it
print ('Length of text: {} characters'.format(len(text)))

# Take a look at the first 250 characters in text
print(text[:250])
