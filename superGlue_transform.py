import cv2
import torch
import numpy as np
# import imageio
from models.matching import Matching


torch.set_grad_enabled(False)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')


def image2tensor(img:np.ndarray, device:torch.device) -> torch.Tensor:
    gray = cv2.cvtColor(img, 6).astype('float32')
    # convert to torch tensor
    return torch.from_numpy(gray/255.).float()[None, None].to(device)


config = {
    'superpoint': {
        'nms_radius': 3,
        'keypoint_threshold': 0.005,
        'max_keypoints': 1024
    },
    'superglue': {
        'weights': 'indoor',   # choices={'indoor', 'outdoor'}
        'sinkhorn_iterations': 20,
        'match_threshold': 0.2,
    }
}


matching = Matching(config).eval().to(device)

# Load the image pair.
img0 = '/home/agent/Documents/Project/Vision/data/foto1A.jpg'
img1 = '/home/agent/Documents/Project/Vision/data/foto1B.jpg'
image0 = cv2.imread(img0)
image1 = cv2.imread(img1)
# image0 = imageio.imread('http://www.ic.unicamp.br/~helio/imagens_registro/foto1A.jpg')
# image1 = imageio.imread('http://www.ic.unicamp.br/~helio/imagens_registro/foto1B.jpg')
h0, w0 = image0.shape[:2]
h1, w1 = image1.shape[:2]

inp0 = image2tensor(image0, device)
inp1 = image2tensor(image1, device)


#NOTE Perform the matching.
pred = matching({'image0': inp0, 'image1': inp1})
pred = {k: v[0].cpu().numpy() for k, v in pred.items()}
kpts0, kpts1 = pred['keypoints0'], pred['keypoints1']
matches, conf = pred['matches0'], pred['matching_scores0']

#NOTE Keep the matching keypoints.
valid = matches > -1
mkpts0 = kpts0[valid]
mkpts1 = kpts1[matches[valid]]
mconf = conf[valid]

#NOTE sorted point from high confident to low confident
m_pointes = list(zip(mkpts0, mkpts1, mconf))
m_pointes = sorted(m_pointes, key=lambda x: x[2], reverse= True)
mkpts0, mkpts1, mconf = list(zip(*m_pointes))

# choose 10% matching point with highest confident to align image
n_keypoints = max(4, int(0.12*len(mconf)))
mkpts0 = mkpts0[:n_keypoints]
mkpts1 = mkpts1[:n_keypoints]

# NOTE 3. Perspectivate transform - estimate homography matrix
# Estimate homography matrix with RANSAC.
H, status = cv2.findHomography(np.float32(mkpts0),
                               np.float32(mkpts1), cv2.RANSAC)

result = cv2.warpPerspective(image0, H, (w0+w1, h0))
result[0:h1, 0:w1] = image1
cv2.imshow('fwa', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
# cv2.imwrite("stiching_img.jpg", result)
