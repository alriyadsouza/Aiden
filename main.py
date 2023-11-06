import spacy
import pandas as pd
from sys import exit

from patient import Patient

nlp = spacy.load("en_core_web_sm")

bookings = pd.read_csv("booking.csv")
patients = pd.read_csv("dataset.csv")

def get_int(question):
    while True:
        try:
            p_id = int(input(question))
            if p_id < 1:
                raise ValueError
            return p_id

        except ValueError:
            continue

def ask_yes_no(input_str):
    doc = nlp(input(input_str))
    
    positive_keywords = ["yes", "yeah", "yep", "yup", "definitely", "absolutely"]
    negative_keywords = ["no", "nope", "nah", "not really", "negative"]
    
    for token in doc:
        if token.lower_ in positive_keywords:
            return True
        elif token.lower_ in negative_keywords:
            return False
    
    return False

def get_patient(p_id):
    return patients[patients['PatientId'] == p_id]

def get_next_id():
    return patients['PatientId'].max() + 1

def identify_gender(text):
    doc = nlp(text)

    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            for token in ent:
                if token.pos_ == 'PRON' and token.text.lower() == 'he':
                    return 'M'
                elif token.pos_ == 'PRON' and token.text.lower() == 'she':
                    return 'F'

def get_gender():
    gender_input = input("Please enter your gender: ")
    return identify_gender(gender_input)

def make_patient():
    return Patient(
        input("Enter your full name: "),
        get_next_id(),
        get_gender(),
        get_int("Please enter your age: ")
    )

def main():
    print("Hi there, I am Aiden. Your personal health assistant!")
    need_help = ask_yes_no("Do you need assistance concerning your health? ")

    if not need_help:
        exit("Let me know if you need help anytime.")

    is_previous_patient = ask_yes_no("Have you used our service prior to this? ")

    if is_previous_patient:
        p_id = get_patient_id("Please enter patient ID: ")
        patient = get_patient(p_id)
    else:
        patient = make_patient()

if __name__ == "__main__":
    main()