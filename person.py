import random
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection = None):
        self._id = _id  # int
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        self.survived = self.did_survive_infection()

    def did_survive_infection(self):
        """Checks if person survives infection"""
        if self.infection is not None:
            check_survival = random.random()
            if check_survival < self.infection.mortality_rate:
                return False
            else:
                self.is_vaccinated = True
                self.infection = None
                return True
