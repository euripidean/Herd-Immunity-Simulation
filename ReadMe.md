# Final Project: Herd Immunity Simulation

## The Project
A simuation that allows the user to test pandemic outcomes based on criteria such as population size, %of population vaccinated, virus r number and mortality rate. The simulation will output an outcome, along with all steps taken during interactions between infected and non-infected members of the population.

## How to Run
$git python3 simulation.py
And then enter the values as prompted by arg parser.

## Notes on Logic
- When the population is created, it's necessary to set the intially infected as 'vaccinated' in order for successful burn out of the virus.
- Because of the create_population() method, it's also best not to have self._survives() run as the Person objects are instantiated as the initially infected may not survive being created, which means the rest of the expected results would be altered. Instead, I chose to run this method during the interactions.
- In terms of calculating the number of fatalities/vaccinated I chose to append these People to new lists as part of the process, as the instructions in some places referred to having an is_alive attribute and in other places didn't (I assume the assignment was re-written post COVID and some stuff was accidentally left in, but deleted elsewhere. Understandable!) 

## Learning
- Use a log file for outputs was very cool!
- Having a more complex program makes testing and finding errors much more difficult


