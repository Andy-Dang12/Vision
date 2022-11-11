import torch, os
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToTensor, Resize, Compose
from torch.utils.data import DataLoader


path = '/home/tz/Downloads/data/14_11'
# trans = Compose([Resize([112, 112]), ToTensor()])
trans = ToTensor()
dataset = ImageFolder(path, transform=trans)
dataLoader = DataLoader(dataset, 1, num_workers=os.cpu_count())


def get_mean_and_std(dataloader:DataLoader):
    channels_sum, channels_squared_sum, num_batches = 0, 0, 0
    for data, _ in dataloader:
        # Mean over batch, height and width, but not over the channels
        channels_sum += torch.mean(data, dim=[0, 2, 3])
        channels_squared_sum += torch.mean(data**2, dim=[0, 2, 3])
        num_batches += 1
    
    mean = channels_sum / num_batches

    # std = sqrt(E[X^2] - (E[X])^2)
    std = (channels_squared_sum / num_batches - mean ** 2) ** 0.5

    return mean, std

from time import time

s = time()
mean, std = get_mean_and_std(dataLoader)
ss = time()
print(mean)
print(std)
print(ss-s)
