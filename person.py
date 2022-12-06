import random
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection = None):
        self._id = _id  # int
        self.is_vaccinated = is_vaccinated
        self.infection = infection
        #Note: the instructions didn't include is_alive as a person attribute so my solution was developed without it. 
        #Instead I move the person to the fatalities list if they pass away.

    def did_survive_infection(self):
        """Checks if person survives infection"""
        if self.infection is not None:
            check_survival = random.random()
            if check_survival < self.infection.mortality_rate:
                return False
            else:
                self.is_vaccinated = True
                return True

if __name__ == "__main__":
   #Test 1
    vaccinated_person = Person(1, True)
    assert vaccinated_person._id == 1
    assert vaccinated_person.is_vaccinated is True
    assert vaccinated_person.infection is None

    # Test 2
    unvaccinated_person = Person(2, False)
    assert unvaccinated_person._id == 2
    assert unvaccinated_person.is_vaccinated is False
    assert unvaccinated_person.infection is None

    # Test 3
    virus = Virus("Dysentery", 0.7, 0.2)
    infected_person = Person(3, False, virus)
    assert infected_person._id == 3
    assert infected_person.is_vaccinated is False
    assert infected_person.infection is virus

    

