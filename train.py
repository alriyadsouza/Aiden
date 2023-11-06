import re
import random
import pandas as pd
import string
import random
import nltk
from transformers import pipeline
import tkinter as tk
from datetime import datetime

class Aiden:
  negative_response=("no","nope",'Never', 'Not now', 'Not yet', "nah", "naw",'Not possible', 'Dont', 'Stop', 'Nevermind', 'Sorry')
  exit_commands =("quit", "pause", "exit", "goodbye", "bye", "later","End" )
  starter_questions = (
    "How can I assist you today?",
    "What brings you here?",
    "Is there something specific you'd like to discuss?",
    "How are you feeling today?",
    "Do you have any questions about your upcoming appointment?",
    "How may I help improve your experience?",
    "Are you looking to schedule an appointment?",
    "Do you need assistance with any medical concerns?",
    "Is there a specific specialist you would like to consult?",
    "How can I make your healthcare journey smoother?"
  )

  def __init__(self):
    self.aidable = {'patient_id': r'My id is.*',
                    'new_patient': r'.*new patient.*'}

  def greet(self):
    self.name= input("What is your name?\n")
    will_help= input(f"Hi {self.name}, I am Aiden. Are you new here?\n")
    if will_help.lower() in self.negative_response:
      print("Cool! We'll look into the booking process then :)\n")
      self.search_id()
    else:
      df = pd.read_csv('merged_dataset_with_diseases.csv')
      dff = pd.read_csv('booking.csv')
      gender = input("Hi! How can I assist you today? What is your gender?\n")
      age = input("Great! Could you please tell me your age?\n")
      neighborhood = input("What is your neighborhood?\n")
      scholarship = self.convert_response_to_bool(input("Do you have any scholarship? If yes, please provide the details.\n"))
      selected_disease_types = self.display_disease_types(df['disease_type'].unique())
      selected_disease = selected_disease_types[0]
      hipertension = self.convert_response_to_bool(input("Do you have Hypertension?\n"))
      diabetes = self.convert_response_to_bool(input("Do you have Diabetes?\n"))
      alcoholism = self.convert_response_to_bool(input("Do you have Alcoholism?\n"))
      handcap = self.convert_response_to_bool(input("Are u Handicaped?\n"))
      speciality = self.get_speciality(selected_disease)
      df = pd.read_csv('merged_dataset_with_diseases.csv')  
      last_patient_id, last_appointment_id = self.get_last_ids(df)
      next_patient_id = last_patient_id + 1
      next_appointment_id = last_appointment_id + 1

      today = datetime.now()
      data = {
                'PatientId': [next_patient_id],  
                'AppointmentID': [next_appointment_id],  
                'Gender': [gender],
                'ScheduledDay': [today.strftime('%Y-%m-%d')],
                'AppointmentDay': [None],  
                'Age': [age],
                'Neighbourhood': [neighborhood],
                'Scholarship': [scholarship],
                'Hipertension': [hipertension],
                'Diabetes': [diabetes],
                'Alcoholism': [alcoholism],
                'Handcap': [handcap],
                'SMS_received': [None],
                'No-show': [None],
                'Doctor_id': [None],
                'Doctor\'s Name': [None],
                'speciality': [speciality],
                'time':[None],
                'disease_type': [selected_disease]
            }

      dff = pd.DataFrame(data)
      dff.to_csv('booking.csv', mode='a', header=False, index=False)

      #self.chat()
  def get_speciality(self, selected_disease):
    disease_specialty_map = {
    "Cardiologist": ["Coronary artery disease", "Arrhythmia"],
    "Dermatologist": ["Acne", "Eczema"],
    "Orthopedic Surgeon": ["Fractures", "Osteoarthritis"],
    "Gynecologist": ["Polycystic ovary syndrome (PCOS)", "Endometriosis"],
    "Neurologist": ["Migraine", "Multiple sclerosis"],
    "Psychiatrist": ["Depression", "Anxiety disorders"],
    "Oncologist": ["Chemotherapy", "Radiation therapy"],
    "Gastroenterologist": ["Irritable bowel syndrome (IBS)", "Gastroesophageal reflux disease (GERD)"],
    "Pediatrician": ["Childhood vaccinations", "Asthma in children"],
    "Ophthalmologist": ["Cataracts", "Glaucoma"]
    }
    for specialty, diseases in disease_specialty_map.items():
        if selected_disease in diseases:
            return specialty
    return None
      
  def convert_response_to_bool(self, response):
    return 1 if response.lower() not in self.negative_response else 0
      
  def get_last_ids(self, df):
        last_patient_id = df['PatientId'].max()
        last_appointment_id = df['AppointmentID'].max()
        return last_patient_id, last_appointment_id
  
  def make_exit(self,reply):
    for command in self.exit_commands:
      if reply == command:
        print("Thank You! Have a great day!")
        return True

  def chat(self):
    reply= input(random.choice(self.starter_questions)). lower()
    while not self.make_exit(reply):
      reply = input(self.match_reply(reply))

  def match_reply(self, reply):
    for key, value in self.aidable.items():
      intent = key
      regex_pattern= value
      found_match =re.match(regex_pattern, reply)
      if found_match and intent == 'patient_id':
        return self.describe()
      elif found_match and intent =='new_patient':
        return self.describe2()
    if not found_match:
      return self.no_match_intent()

  def search_id(self):
        patient_id = int(input("Enter your patient ID: "))
        df = pd.read_csv('merged_dataset_with_diseases.csv')  # Assuming you have a CSV file named 'merged_dataset_with_diseases.csv'
        filtered_data = df[df['PatientId'] == patient_id]
        if not filtered_data.empty:
          disease_type = filtered_data['disease_type'].iloc[0]  # Assuming the column name is 'disease_type'
          responses = (
            "Would you like to schedule your appointment for {disease_type} like the one you did before?\n",
            "Are you interested in arranging your appointment for {disease_type} as we previously discussed?\n",
            "Shall we book your appointment for {disease_type} similar to the last one?\n",
            "Would you prefer to set up your next appointment for {disease_type} like the previous one?\n",
            "Do you want to plan your upcoming appointment for {disease_type} just as we did earlier?\n"
          )
          response = random.choice(responses)
          print(response.format(disease_type=disease_type))
          if response not in self.negative_response:
            print("")
          else:
              #treatment=input("What other treatment are you wishing to look at?")
              selected_disease_types = self.display_disease_types(df['disease_type'].unique())
              print("Selected Disease Types:", selected_disease_types)
        else:
            print("Patient ID not found. Please enter a valid ID.")

  def display_disease_types(self, disease_types):
        root = tk.Tk()
        root.title("Select Disease Type")
        
        selected_diseases = []

        def on_checkbox_click(disease, var):
            if var.get() == 1:
                selected_diseases.append(disease)
            elif var.get() == 0 and disease in selected_diseases:
                selected_diseases.remove(disease)

        var_list = []
        for disease in disease_types:
            var = tk.IntVar()
            var_list.append(var)
            checkbox = tk.Checkbutton(root, text=disease, variable=var, onvalue=1, offvalue=0, command=lambda disease=disease, var=var: on_checkbox_click(disease, var))
            checkbox.pack(anchor='w')

        ok_button = tk.Button(root, text="OK", command=root.destroy)
        ok_button.pack()

        root.mainloop()

        # Now selected_diseases will contain the list of selected diseases
        print("Selected Diseases:", selected_diseases)
        return selected_diseases


Aiden= Aiden()
Aiden.greet()
