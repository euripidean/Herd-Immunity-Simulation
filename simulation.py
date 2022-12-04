import random, math
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    """Simulation Object"""
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.logger = Logger('Logfile')
        self.people = self._create_population()
        self.newly_infected = []
        self.time_step_number = 0
        self.interactions = 0

    def _create_population(self):
        """Method to create population - infected and uninfected"""
        people = []
        infected_people = []
        id = 0
        #Deal with infected people first: NOTE: this will run self.survived, so some initially infected may die before loop 1
        for i in range(self.initial_infected):
                infected_people.append(Person(id,False,self.virus))
                id += 1
        #reset Id number
        id = self.initial_infected + 1
        #Now deal with uninfected
        uninfected_people = []
        for j in range(self.pop_size - self.initial_infected):
                uninfected_people.append(Person(id,False))
                id += 1
        #Now deal with vaccinated percentage
        vaccinated_number = len(uninfected_people) * self.vacc_percentage
        vaccinated_number = math.floor(vaccinated_number)
        #set vaccination status of uninfected folks based on %
        for v in range(vaccinated_number):
            uninfected_people[v].is_vaccinated = True

        #Combine infected and uninfected
        people = people + uninfected_people + infected_people
        #return the list of people to the Simulation object
        return people
            
    def _simulation_should_continue(self):
        """Check if simulation can continue"""
        #check vaccinated:
        vaccinated = 0
        for person in self.people:
            if person.is_vaccinated:
                vaccinated += 1
        survivors = 0
        #check survivors
        for person in self.people:
            if person.survived is not False:
                survivors += 1

        while vaccinated < len(self.people) or survivors > 0:
            print(f"Vaccinated: {vaccinated}")
            print(f"Survivors: {survivors}")
            return True
        return False

    def run(self):
        """Run simulation, checking for if simulation should continue. Logs metadata and final outcome."""
        #Set up simulation
        self.time_step_number = 1
        should_continue = True

        #Write Simulation Metadata to file
        self.logger.write_metadata(
            self.pop_size, 
            self.vacc_percentage, 
            self.virus.name, 
            self.virus.mortality_rate, 
            self.virus.repro_rate
            self.initial_infected)

        #Run while simulation should continue
        while should_continue:
            self.time_step()
            self.time_step_number += 1
            should_continue = self._simulation_should_continue()

        #Send over final data after simulation has completed
        self.logger.send_final_data()
        

    def time_step(self):
        """Each time step, all infected people interact with 100 random people."""
        random_people = []
        infected_people = []
        outcomes = [0,0,0]

        #reset interactions:
        self.interactions = 1

        #get infected people
        for person in self.people:
            if person.infection is not None:
                infected_people.append(person)

        while len(infected_people) > 0:
            #Get first infected person
            infected_person = infected_people[0]
            #remove infected person from self.people as they can't interact with themselves
            self.people.pop(self.people.index(infected_person))

            for i in range (100):
                random_person = random.choice(self.people)
                self.interaction(infected_person, random_person, outcomes)
                #remove random person from people list temporarily so they can't interact twice in one loop
                self.people.pop(self.people.index(random_person))
                #add them to the random people list for reintegration with population at the end of the loop
                random_people.append(random_person)

            #100 people have been interacted with
            self.people += random_people
            #clear out random people list:
            random_people = []
            #add infected person back into self.people
            self.people.append(infected_person)
            #remove infected person from infected list
            infected_people.pop(0)
        print('All infected people looped through')

        #END OF TIME STEP

        #Summarise interactions
        self.logger.interaction_summary(self.time_step_number, self.interactions, len(self.newly_infected), outcomes)
        #Now infect newly infected people
        self._infect_newly_infected()
        return

    def interaction(self, infected_person, random_person, outcomes):
        """Each interaction between infected and random person"""
        self.interactions += 1
        if random_person.is_vaccinated or random_person.infection is not None:
            if random_person.is_vaccinated:
                outcomes[0] += 1
            else:
                outcomes[1] += 1
            return
        elif not random_person.is_vaccinated:
            gets_infected = random.random()
            if gets_infected < self.virus.repro_rate:
                self.newly_infected.append(random_person)
            else:
                outcomes[2] += 1
                return

    def _infect_newly_infected(self):
        """Give virus to all newly infected People"""
        fatalities = 0
        for i in range(len(self.newly_infected)):
            new_infected_person = self.newly_infected[i]
            new_infected_person.infection = self.virus
            if self.newly_infected[i].survived is not True:
                print('Newly infected person died')
                fatalities += 1
                self.pop_size = len(self.people)
        self.logger.log_infection_survival(self.time_step_number, self.pop_size, fatalities)
        self.newly_infected = []
        return


if __name__ == "__main__":
    # Test your simulation here
    # virus_name = "Sniffles"
    # repro_num = 0.5
    # mortality_rate = 1
    # virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.5
    initial_infected = 4

    # Make a new instance of the imulation
    virus = Virus('Ebola',0.25,0.7)
    sim = Simulation(virus,pop_size,vacc_percentage,initial_infected)

    sim._create_population()
    sim.run()

