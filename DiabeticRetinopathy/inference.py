# Ignore  the warnings
import warnings

warnings.filterwarnings('always')
warnings.filterwarnings('ignore')

# data visualisation and manipulation
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# configure
# sets matplotlib to inline and displays graphs below the corressponding cell.

from sklearn.metrics import confusion_matrix

# specifically for manipulating zipped images and getting numpy arrays of pixel values of images.
import cv2
import numpy as np
# from tqdm import tqdm, tqdm_notebook
# import os, random
# from random import shuffle
# from zipfile import ZipFile
# from PIL import Image
# from sklearn.utils import shuffle
import sys

import fastai
from fastai import *
from fastai.vision import *
from fastai.callbacks import *
from fastai.basic_train import *
from efficientnet_pytorch import EfficientNet
from fastai.vision.learner import *








model = EfficientNet.from_name('efficientnet-b6', override_params={'num_classes': 5 })


class FocalLoss(nn.Module):
    def __init__(self, gamma=3., reduction='mean'):
        super().__init__()
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        CE_loss = nn.CrossEntropyLoss(reduction='none')(inputs, targets)
        pt = torch.exp(-CE_loss)
        F_loss = ((1 - pt)**self.gamma) * CE_loss
        if self.reduction == 'sum':
            return F_loss.sum()
        elif self.reduction == 'mean':
            return F_loss.mean()

from torch.utils.data.sampler import WeightedRandomSampler

class OverSamplingCallback(LearnerCallback):
    def __init__(self,learn:Learner, weights:torch.Tensor=None):
        super().__init__(learn)
        self.labels = self.learn.data.train_dl.dataset.y.items
        _, counts = np.unique(self.labels, return_counts=True)
        self.weights = (weights if weights is not None else
                        torch.DoubleTensor((1/counts)[self.labels]))

    def on_train_begin(self, **kwargs):
        self.learn.data.train_dl.dl.batch_sampler = BatchSampler(
            WeightedRandomSampler(self.weights, len(self.learn.data.train_dl.dataset)),
            self.learn.data.train_dl.batch_size,False)

path=''
learn = load_learner(path)

data1 = [['00a8624548a9',0],['00b74780d31d',0],['000c1434d8d7',0],['0d0a21fd354f',0]]
df_train = pd.DataFrame(data1, columns=['id_code','diagnosis'])

aptos19_stats = ([0.42, 0.22, 0.075], [0.27, 0.15, 0.081])
train_path19 = Path('')
data = ImageDataBunch.from_df(df=df_train,
                              path=train_path19, folder='imagelist', suffix='.png',
                              ds_tfms=get_transforms(flip_vert=False),
                              size=356
                             ).normalize(aptos19_stats)

img = data.train_ds[1][0]
print(learn.predict(img))