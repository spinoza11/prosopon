import random
import time
import tkinter as tk
from datetime import datetime

import numpy as np
from PIL import ImageTk

from load_dataset import dataset


class session:
   def new_try(self):
      self.people.choose_new_people()
      #print(self.people.group)
      self.impostor_spot = random.choice(self.places)
      #print("impostor spot: " ,self.impostor_spot)
      self.button_list=[]
      self.image_list = []
      self.is_impostor = [0,0,0]
      self.group_images = self.people.load_group()
      for spot in self.places:
         if spot==self.impostor_spot:
            self.is_impostor[spot] = 1
            self.image_list.append(ImageTk.PhotoImage(self.people.load_impostor()))
            self.button_list.append(tk.Button(self.root,image= self.image_list[-1],border=0,command=lambda: self.choice(1)))
            self.button_list[-1].grid(row=0,column=spot)
         else:
            #is_impostor=0
            self.image_list.append(ImageTk.PhotoImage(self.group_images.pop(random.choice(range(len(self.group_images))))))
            self.button_list.append(tk.Button(self.root,image= self.image_list[-1],border=0,command=lambda: self.choice(0)))
            self.button_list[-1].grid(row=0,column=spot)

   def start_session(self):
      self.bottom_button.grid_remove()
      self.add_stop_button()
      self.try_number=0
      self.session_successes = []
      self.new_try()

   def stop_session(self):
      for button in self.root.grid_slaves():
         button.grid_forget()
         button.destroy()
      self.button_list=[]
      print(self.root.grid_slaves())
      self.add_start_button()
      if self.try_number>=self.session_size:
         self.save_session()

   def save_session(self):
      with open(self.score_file,"a+") as f:
         f.write(f"Date: { datetime.today().strftime('%Y-%m-%d')}\nDataset: {self.people.dataset_address}\nscore: {np.average(self.session_successes)}\nsession length: {self.session_size}\n\n")

   def set_bottom_button(self,button_name,function):
      self.bottom_button = tk.Button(self.root, text = f"{button_name} training",fg='white',border=0,font="Helvetica 14",relief='flat' ,\
                activebackground='#888888', bg = '#888888',command = function, padx=20,pady=10)
      self.bottom_button.grid(row=1,column=0)

   def add_start_button(self):
      self.set_bottom_button("Start",self.start_session)

   def add_stop_button(self):
      self.set_bottom_button("Stop",self.stop_session)

   def __init__(self) -> None:
      self.session_size=100
      self.score_file = "score_history.csv"
      self.root = tk.Tk()
      self.root.configure(background="#666666")
      self.root.title('Prosopon: face recognition training') 
      self.root.grid()
      self.people = dataset()
      self.places = range(3)
      self.add_start_button()
      self.root.mainloop()

   def choice(self,is_impostor):
      self.try_number+=1
      print("correct choice: ",(bool)(is_impostor))
      self.session_successes.append(is_impostor)
      if not is_impostor:
         print(f"Not the impostor! impostor is {self.people.impostor}, you clicked on {self.people.group}")
      print("Succes rate: ",np.average(self.session_successes),"\n")
      if self.try_number<self.session_size:
         self.new_try()
      else:
         self.stop_session()

if __name__=="__main__":   
   session()


   

      
      
