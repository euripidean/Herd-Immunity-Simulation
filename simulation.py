import random, sys
# random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        # TODO: Create a Logger object and bind it to self.logger.
        # Remember to call the appropriate logger method in the corresponding parts of the simulation.
        self.virus = virus
        self.pop_size = pop_size
        self.vacc_percentage = vacc_percentage
        self.initial_infected = initial_infected
        self.logger = Logger('Logfile')
        self.people = self._create_population()
        self.newly_infected = []

    def _create_population(self):

        people = []
        id = 0
        #Deal with infected people first
        for i in range(self.initial_infected):
                infected_people = Person(id,False,self.virus)
                people.append(infected_people)
                id += 1
        #reset Id number
        id = self.initial_infected + 1
        #Now deal with unifected
        for j in range(self.pop_size - self.initial_infected):
                uninfected_people = Person(id,False)
                people.append(uninfected_people)
                id += 1
        #return the list of people to the Simulation object
        return people
            
       

               

    def _simulation_should_continue(self):
        survivors = len(self.people)
        vaccinated = 0
        while survivors > 0 or vaccinated < len(self.people):
            for person in self.people:
                if person.survived != True:
                    survivors -= 1
                if person.is_vaccinated != False:
                    vaccinated += 1
            return True
        return False

    def run(self):
        # This method starts the simulation. It should track the number of 
        # steps the simulation has run and check if the simulation should 
        # continue at the end of each step. 

        time_step_counter = 0
        should_continue = True

        while should_continue:
            self.time_step()
            time_step_counter += 1
            should_continue = self._simulation_should_continue()

        #Not sure if this needs to be in the while loop or not.
        self.write_metadata(
            self.pop_size, 
            self.vacc_percentage, 
            self.virus.name, 
            self.virus.mortality_rate, 
            self.virus.repro_rate)
        
        # TODO: When the simulation completes you should conclude this with 
        # the logger. Send the final data to the logger. 
        #NOT SURE WHAT THIS MEANS - What final data?

    def time_step(self):
        # This method will simulate interactions between people, calulate 
        # new infections, and determine if vaccinations and fatalities from infections
        # The goal here is have each infected person interact with a number of other 
        # people in the population
        alive_people = []
        random_people = []
        infected_people = []
        #create list of alive people as dead people can't be interacted with
        for person in self.people:
            if person.survived:
                alive_people.append(person)
            if person.infection is not None:
                infected_people.append(person)
        print("**************************************")
        print(f"initial population = {self.pop_size}")
        print(f"number of people: {len(self.people)}")
        print("**************************************")
        print(f"length of alive people: {len(alive_people)}")
        print(f"length of infected people: {len(infected_people)}")
        
        # now loop through list of alive people
        while len(infected_people) > 0:
            print('&&& START OF WHILE LOOP %%%')
            #get first infected person from infected people list
            infected_person = infected_people[0]
            #remove them temporarily from the list of alive people so they don't randomly interact with themselves
            alive_people.pop(infected_person._id)
            # 100 times, get a random other person and interact with them
            for i in range (0,10):
                random_id = random.randint(0, len(alive_people))
                random_person = alive_people[random_id]
                self.interaction(infected_person, random_person)
                print("Back from interation, popping random person from alive list")
                #remove random person from alive people so they can't interact twice
                alive_people.pop(random_id)
                #add them to the random people list for reintegration with population at the end of the loop
                random_people.append(random_person)
                print(f"random list now has {len(random_people)} on it")
            #add random people list back to general alive population
            print(f"Final random list has {len(random_people)} on it.")
            alive_people += random_people
            #clear out random people list:
            random_people = []
            print(f"Alive people list is restored to: {len(alive_people)}.")
            #remove infected person from list
            infected_people.pop(0)
            print(f"Infected people list length: {len(infected_people)}")

        #UP TO HERE. LOOKS LIKE LOOP IS ONLY RUNNING ONCE.

        print('outside of the loop through alive people')
                
                




        # TODO: Loop over your population
        # For each person if that person is infected
        # have that person interact with 100 other living people 
        # Run interactions by calling the interaction method below. That method¡
        # takes the infected person and a random person
        pass

    def interaction(self, infected_person, random_person):
        print("inside interaction")
        return
        # TODO: Finish this method.
        # Get possible interactions
        # The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0.0 and 1.0.  If that number is smaller
            #     than repro_rate, add that person to the newly infected array
            #     Simulation object's newly_infected array, so that their infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call logger method during this method. WHICH ONE?!
        pass

    def _infect_newly_infected(self):
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    # Test your simulation here
    virus_name = "Sniffles"
    repro_num = 0.5
    mortality_rate = 0.12
    virus = Virus(virus_name, repro_num, mortality_rate)

    # Set some values used by the simulation
    pop_size = 1000
    vacc_percentage = 0.1
    initial_infected = 10

    # Make a new instance of the imulation
    virus = Virus('COVID-19',3,0.08)
    sim = Simulation(virus,pop_size,vacc_percentage,2)

    sim._create_population()
    sim.time_step()
