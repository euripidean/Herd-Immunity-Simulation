class Virus(object):
    """Virus Object"""
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate

# Class Testing
if __name__ == "__main__":
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3

#Additional Test 1
    virus2 = Virus("Ebola", 0.25, 0.7)
    assert virus2.name == "Ebola"
    assert virus2.repro_rate == 0.25
    assert virus2.mortality_rate == 0.7

#Additional Test 2
    virus3 = Virus("Lassa Fever", 0.6, 0.4)
    assert virus3.name == "Lassa Fever"
    assert virus3.repro_rate == 0.6
    assert virus3.mortality_rate == 0.4
