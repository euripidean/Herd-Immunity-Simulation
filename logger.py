from datetime import date
class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name


    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num, initial_infected):
        sim_date = date.today()
        f = open(self.file_name, 'a')
        f.write(f""" Population: {pop_size}\tVaccination %: {vacc_percentage}\t Virus Name: {virus_name}\tMortality Rate: {mortality_rate}\tR Number: {basic_repro_num}\tInitial Infected: {initial_infected}\t Simulation Date: {sim_date}\n""")

    def interaction_summary(self, time_step, number_of_interactions, number_of_new_infections, outcomes, infected_people):
        design = '*' * 40
        f = open(self.file_name, 'a')
        f.write(f"""
        {design}
        INTERACTION SUMMARY:\n
        Time Step: {time_step}\n
        Number of Interactions : {number_of_interactions}\n
        Number of infected people in population: {infected_people}\n
        New Infections : {number_of_new_infections}\n
        Immune Interaction : {round(outcomes[0]/number_of_interactions,2)*100}%\n
        Unvaccinated but no infection after Interaction : {round(outcomes[1]/number_of_interactions,2)*100}%\n
        """)

    def log_infection_survival(self, step_number, population_count, number_of_new_fatalities, newly_vaccinated, total_vaccinated, original_pop):
        design = '-' * 40
        f = open(self.file_name, 'a')
        f.write(f"""
        {design}
        Step Number {step_number}\n
        Current population count = {population_count}\n
        Number of new fatalities = {number_of_new_fatalities}\n
        Number of infected survivors = {newly_vaccinated}\n
        Total Immune: {total_vaccinated}\n
        Total Fatalities: {original_pop - population_count}\n
        """)

    def send_final_data(self, step_number, original_pop, pop_size, fatalities_list, vaccinated_list, sim_outcome, total_interactions):
        design = '#' * 40
        total_infected = 0
        fatalities = len(fatalities_list)
        vaccinated = len(vaccinated_list)
        #Find total infected:
        for person in fatalities_list:
            total_infected += 1

        for person in vaccinated_list:
            if person.infection is not None:
                total_infected += 1


        if pop_size > 0:
            survivors = f"{(pop_size/original_pop) * 100} %"
        else:
            survivors = 'There were no survivors.'
        f = open(self.file_name, 'a')
        f.write(f"""
        {design}
        SIMULATION COMPLETE: FINAL SUMMARY\n
        Total number of steps in simulation: {step_number}\n
        % of Population that survived: {survivors}\n
        % of Population Fatalities: {(fatalities/original_pop)*100}%\n
        % of Population that was infected: {(total_infected/original_pop) *100}%\n
        Total Number of interactions where vaccination/immunity prevented infection: {sim_outcome} out of {total_interactions} interactions.\n 
        Total Fatalities: {fatalities}\n
        Total Immune by end of Simulation: {vaccinated}\n
        {design}
        """)
