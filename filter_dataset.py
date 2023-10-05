import os

import numpy as np
from load_dataset import dataset, listdir_full
from PIL import Image


def filter_small_images(data,min_size):
   """
   removes images with width/height smalle than min_size
   """
   width = []
   height = []
   for person in data.people:
      images_addresses =listdir_full(data.people[person])
      for image_address in images_addresses:
         image = Image.open(image_address)
         width.append(image.width)
         height.append(image.height)
         if image.height<min_size and image.width<min_size:
            print(data.people[person])
            image.close()
            os.remove(image_address)
         else:
            image.close()
   print(np.average(width),np.average(height))

def filter_empty_folders(data:dataset):
   for person in data.people:
      images_addresses =listdir_full(data.people[person])
      if not len(images_addresses):
         print(person)
         os.rmdir(data.people[person])

if __name__=="__main__":
   address = "C:/Users/blanche.jay/Documents/filtered_archive/lfw_cut"
   data=dataset(address)
   filter_small_images(data,80)
   filter_empty_folders(data)