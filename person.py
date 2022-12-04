import random
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection = None):
        self._id = _id  # int
        self.is_vaccinated = is_vaccinated
        self.infection = infection

    def did_survive_infection(self):
        """Checks if person survives infection"""
        if self.infection is not None:
            check_survival = random.random()
            if check_survival < self.infection.mortality_rate:
                return False
            else:
                self.is_vaccinated = True
                return True

virus = Virus('Ebola', 0.25,0.6)

people = []

for i in range(1, 1000):
    person = Person(i,False,virus)
    people.append(person)

# Now that you have a list of 100 people. Resolve whether the Person 
# survives the infection or not by looping over the people list. 

did_survive = 0
died = 0

for person in people:
    # For each person call that person's did_survive_infection method
    survived = person.did_survive_infection()
    if survived:
        did_survive += 1
    else:
        died += 1

print(f"Died: {died} | Survived: {did_survive}") 

