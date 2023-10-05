import os
import random

from PIL import Image

"""
ToDo:
 - filter dataset (low quality images)
 - tag per gender, ethnicity and age group
 - filter same image

"""


def listdir_full(dir_path,include = None,avoid = None):
   if include:
      return [f"{dir_path}/{i}" for i in os.listdir(dir_path) if include in i]
   if avoid:
      return [f"{dir_path}/{i}" for i in os.listdir(dir_path) if avoid not in i]
   return [f"{dir_path}/{i}" for i in os.listdir(dir_path)]

class dataset:
   def __init__(self,address="C:/Users/blanche.jay/Documents/filtered_archive/lfw_cut") -> None:
      self.dataset_address = address
      self.people = {}
      self.people_multiple = {}
      self.group = None
      people_folders = listdir_full(address)
      for human in people_folders:
         name = human.split(sep="/")[-1]
         images= listdir_full(human)
         if len(images)>=2:
            self.people_multiple.update({name:human})
         self.people.update({name:human})
      self.choose_impostor()
      self.choose_group()
   
   def choose_group(self):
      self.group = random.choice(list(self.people_multiple.items()))[0]
      return self.group
   
   def choose_impostor(self):
      impostor = random.choice(list(self.people.items()))[0]
      while impostor==self.group:
         impostor = random.choice(list(self.people.items()))[0]
      self.impostor= impostor
      return self.impostor
   
   def choose_new_people(self):
      self.choose_group()
      self.choose_impostor()
      return self.impostor,self.group      

   def __load_images(self,name,n=2):
      images_addresses = listdir_full(self.people[name])
      chosen=[]
      if n==-1:
         n=len(images_addresses)
      for i in range(n):
         chosen.append( random.choice(images_addresses))
         images_addresses.remove(chosen[-1])
      chosen_images = [Image.open(im) for im in chosen ]
      return chosen_images
   
   def load_impostor(self):
      return self.__load_images(self.impostor,n=1)[0]

   def load_group(self):
      return self.__load_images(self.group,n=2)

   def load_all(self,name):
      return self.__load_images(name,-1)

   def subset(self,n=-1,include = lambda i:True,exclude = lambda i:False):
      l=list(self.people.items())
      if n==-1:
         n=len(l)
      res = [i for i in l[0:n] if (include(i)and not exclude(i))]
      self.people_subset = {}
      for person in res:
         self.people_subset.update({person[0]:person[1]})
      return self.people_subset


if __name__=="__main__":
   humans = dataset()
   print(humans.subset(include=lambda name:name[0][0]=="Z"))



      


     




