class Logger(object):
    def __init__(self, file_name):
        # TODO:  Finish this initialization method. The file_name passed should be the
        # full file name of the file that the logs will be written to.
        self.file_name = file_name

    # The methods below are just suggestions. You can rearrange these or 
    # rewrite them to better suit your code style. 
    # What is important is that you log the following information from the simulation:
    # Meta data: This shows the starting situtation including:
    #   population, initial infected, the virus, and the initial vaccinated.
    # Log interactions. At each step there will be a number of interaction
    # You should log:
    #   The number of interactions, the number of new infections that occured
    # You should log the results of each step. This should inlcude: 
    #   The population size, the number of living, the number of dead, and the number 
    #   of vaccinated people at that step. 
    # When the simulation concludes you should log the results of the simulation. 
    # This should include: 
    #   The population size, the number of living, the number of dead, the number 
    #   of vaccinated, and the number of steps to reach the end of the simulation. 

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num, initial_infected):

        f = open(self.file_name, 'a')
        f.write(f"""
        Population: {pop_size}\t
        Vaccination %: {vacc_percentage}\t
        Virus Name: {virus_name}\t
        Mortality Rate: {mortality_rate}\t
        R Number: {basic_repro_num}\t
        Initial Infected: {initial_infected}\n""")


    # def log_interaction(self, interaction_number, infected_person, random_person, outcome):
    #     f = open(self.file_name, 'a')
    #     f.write(f"""*********************\nInteraction Number: {interaction_number} \n
    #     \t Infected Person {infected_person._id} interacted with Person Id: {random_person._id}\n 
    #     Outcome: {outcome}""")

    def interaction_summary(self, time_step, number_of_interactions, number_of_new_infections, outcomes):
        design = '*' * 40
        f = open(self.file_name, 'a')
        f.write(f"""
        {design}
        INTERACTION SUMMARY:\n
        Time Step: {time_step}\n
        Number of Interactions: {number_of_interactions}\n
        New Infection %: {number_of_new_infections}\n
        Interaction but vaccinated %: {round(outcomes[0]/number_of_interactions,2)}%\n
        Interaction but already infected %: {round(outcomes[1]/number_of_interactions,2)}%\n
        Interaction but did not get infected %: {round(outcomes[2]/number_of_interactions,2)}%\n
        """)

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities):
        f = open(self.file_name, 'a')
        f.write(f"""Inside Log Infection Survival""")


    def send_final_data(self):
        pass

    def log_time_step(self, time_step_number):
        f = open(self.file_name, 'a')
        f.write(f"TIME STEP: {time_step_number}")
        pass


test = Logger('test_file')
test.write_metadata(5000,15,'COVID-19',0.01,3)
