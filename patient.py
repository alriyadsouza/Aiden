class Patient:
    def __init__(self, name, p_id, gender, age):
        self.name = name
        self.p_id = p_id
        self.gender = gender
        self.age = age

    def read_ailments(self, ht, db, al, hc):
        self.hypertention = ht
        self.diabetes = db
        self.alcoholism = al
        self.handicap = hc

