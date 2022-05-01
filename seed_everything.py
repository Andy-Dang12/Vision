import numpy as np
import torch
import os
import random
#############################
def seed_everything(seed):
    os.environ['PYTHONHASHSEED'] = str(seed) # set environ
    random.seed(seed) # set python seed
    np.random.seed(seed) # seed the global NumPy RNG
    torch.manual_seed(seed) # seed the RNG for all devices (both CPU and CUDA):
    torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(True)

seed = 152022 # set seed value
seed_everything(seed)