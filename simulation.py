import random, math
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    """Simulation Object"""
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.virus = virus
        self.pop_size = pop_size
        vacc_percentage = vacc_percentage
        initial_infected = initial_infected
        self.logger = Logger('Logfile')
        self.people = self._create_population()
        self.newly_infected = []
        self.time_step_number = 0
        self.original_population = 0
        self.vaccinated = []
        self.fatalities = []

    def _create_population(self):
        """Method to create population - infected and uninfected"""
        self.vaccinated = []
        self.original_population = self.pop_size
        people = []
        infected_people = []
        id = 1
        #Deal with infected people first: 
        for i in range(initial_infected):
                infected_people.append(Person(id,True,self.virus))
                id += 1
        #reset Id number
        id = initial_infected + 1
        #Now deal with uninfected
        uninfected_people = []
        for j in range(self.pop_size - initial_infected):
                uninfected_people.append(Person(id,False))
                id += 1
        #Now deal with vaccinated percentage
        vaccinated_number = len(uninfected_people) * vacc_percentage
        vaccinated_number = math.floor(vaccinated_number)
        #set vaccination status of uninfected folks based on %
        for v in range(vaccinated_number):
            uninfected_people[v].is_vaccinated = True
        
        #Combine infected and uninfected
        people = uninfected_people + infected_people

        #add all vaccinated people to list, including initially infected:
        for person in people:
            if person.is_vaccinated:
                self.vaccinated.append(person)
    
        #return the list of people to the Simulation object
        return people
            
    def _simulation_should_continue(self):
        """Check if simulation can continue"""
        unvaccinated = self.pop_size - len(self.vaccinated)
        number_of_people_alive = self.pop_size

        while unvaccinated > 0 and number_of_people_alive > 0:
            return True
        return False
        
        
    def run(self):
        """Run simulation, checking for if simulation should continue. Logs metadata and final outcome."""
        #Set up simulation
        self.time_step_number = 0
        should_continue = True

        #Write Simulation Metadata to file
        self.logger.write_metadata(
            self.pop_size, 
            vacc_percentage, 
            self.virus.name, 
            self.virus.mortality_rate, 
            self.virus.repro_rate,
            initial_infected)

        #Run while simulation should continue
        should_continue_loop = 0
        while should_continue:
            print(f"--------------------------------------------------------------------------------------")
            self.time_step_number += 1
            self.time_step()
            should_continue = self._simulation_should_continue()
            should_continue_loop += 1

        print(f"End of simulation. Remaining population: {self.pop_size} Number dead: {len(self.fatalities)} Number Vaccinated: {len(self.vaccinated)}\n")
            
        #Send over final data after simulation has completed
        self.logger.send_final_data(self.time_step_number, self.original_population, self.pop_size, len(self.fatalities), len(self.vaccinated))
        

    def time_step(self):
        """Each time step, all infected people interact with max 100 random people."""
        random_people = []
        infected_people = []
        outcomes = [0,0]

        #reset interactions each timestep:
        interactions = 0
        number_of_infected = 0

        #get infected people
        for person in self.people:
            if person.infection is not None:
                infected_people.append(person)
                number_of_infected += 1

        infection_handling = 0
        while len(infected_people) > 0:
            #Get first infected person in list
            infected_person = infected_people[0]
            #remove infected person from self.people as they can't interact with themselves
            self.people.pop(self.people.index(infected_person))
            #set group size
            if self.pop_size >= 100:
                group_size = 100
            else:
                group_size = self.pop_size

            for i in range (group_size):
                random_person = random.choice(self.people)
                interactions += 1
                self.interaction(number_of_infected, random_person, outcomes)
                #remove random person from people list temporarily so they can't interact twice in one loop
                self.people.pop(self.people.index(random_person))
                #add them to the random people list for reintegration with population at the end of the loop
                random_people.append(random_person)

            self.people += random_people
            #clear out random people list:
            random_people = []
            #add infected person back into self.people
            self.people.append(infected_person)
            #remove infected person from infected list
            infected_people.pop(0)

        #END OF TIME STEP
        #Summarise interactions
        self.logger.interaction_summary(self.time_step_number, interactions, len(self.newly_infected), outcomes, number_of_infected)
        #Now infect newly infected people
        self._infect_newly_infected()
        return

    def interaction(self, number_of_infected, random_person, outcomes):
        """Each interaction between infected and random person"""
        if random_person.is_vaccinated or random_person.infection is not None:
                outcomes[0] += 1
                return
        else:
            gets_infected = random.random()
            if gets_infected < self.virus.repro_rate:
                #If person hasn't already been infected, add to newly infected list
                if random_person not in self.newly_infected:
                    self.newly_infected.append(random_person)
            else:
                outcomes[1] += 1
                return

    def _infect_newly_infected(self):
        """Give virus to all newly infected People"""
        #For this batch
        fatality_count = 0
        vaccinated_count = 0

        for i in range(len(self.newly_infected)):
            infected_person = self.newly_infected[i]
            identify = infected_person._id
            #look up in main people list
            for person in self.people:
                if person._id == identify:
                    person.infection = self.virus
                    print(f"{person._id} has been given the virus")
                    #check infection outcome
                    survived = person.did_survive_infection()
            if survived:
                print(f"{person._id} survived and is now vaccinated")
                vaccinated_count += 1
                self.vaccinated.append(person)
            else:
                print(f"{person._id} died")
                fatality_count += 1
                self.pop_size -= 1
                self.fatalities.append(person)
        
        update_population = [i for i in self.people if i not in self.fatalities]
        self.people = update_population



        self.logger.log_infection_survival(
            self.time_step_number, 
            self.pop_size, 
            fatality_count, 
            vaccinated_count,
            len(self.vaccinated),
            self.original_population)

        #clear out newly infected list.
        self.newly_infected = []
        return


if __name__ == "__main__":
    # Test your simulation here
    # Set some values used by the simulation
    pop_size = 100000
    vacc_percentage = 0.9
    initial_infected = 4

    # Make a new instance of the imulation
    virus = Virus('Ebola',0.25,0.7)
    sim = Simulation(virus,pop_size,vacc_percentage,initial_infected)

    sim._create_population()
    sim.run()

