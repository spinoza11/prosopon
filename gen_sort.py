import os

import gender_guesser.detector as gender

from load_dataset import dataset

if __name__ == "__main__":
   data = dataset()
   d = gender.Detector()
   

   counters = {"male":0,"female":0,"mostly_male":0,"mostly_female":0,"unknown":0,"andy":0}
   for person in data.people:
      first_name = person.split("_")[0]
      g = d.get_gender(first_name)
      print(g)
      print(data.people[person])
      os.rename(data.people[person],f"{data.people[person]}__{g}")
      counters[g]+=1
      
   print(counters)
