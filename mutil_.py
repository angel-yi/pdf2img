import hashlib
import os
import random
import shutil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from pdf2img import pdf2img

file_path = '/media/disk1/pdf灰底'

save_path = '/home/siyi/dataset/n2n_e/ori'


pool = ProcessPoolExecutor(max_workers=10)
for pdf in os.listdir(file_path):
    print(pdf)
    img_name = hashlib.md5(str(pdf).encode(encoding='UTF-8')).hexdigest()
    pool.submit(pdf2img, os.path.join(file_path, pdf), save_path, name=img_name, zoom=random.randint(1, 3))
    pdf2img(os.path.join(file_path, pdf), save_path, name=img_name, zoom=random.randint(1, 3))

# imgs = os.listdir(save_path)
# print(len(imgs))
# if len(imgs) < 6900:
#     import sys
#     sys.exit()
# random.shuffle(imgs)
# # imgs  = random.sample(imgs, 13000)
# one_part = int(len(imgs)/100)
# train = imgs[0:one_part*90]
# eval = imgs[one_part*90:]
# print(len(train))
# print(len(eval))
# for i in train:
#     shutil.move(os.path.join(save_path, i), os.path.join('/home/siyi/dataset/n2n_e/train', i))
# for i in eval:
#     shutil.move(os.path.join(save_path, i), os.path.join('/home/siyi/dataset/n2n_e/eval', i))
