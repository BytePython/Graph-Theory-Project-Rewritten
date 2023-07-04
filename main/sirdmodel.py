'''
Rewrite this section only using matrices ()
'''
from time import perf_counter
from copy import deepcopy #used to compare the starting graph with the end result
import logging
import networkx as nx #Adds the networkx package, used to create graph objects
import matplotlib.pyplot as plt #A library to plot graphs
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from lib.infection_class import infection_graph
from lib.infection_strategies import infection_strat,ConstantRateInfection, PersonalInfection, SkillCheckInfection
from lib.gui import userpanel, output_window
from lib.matrix_graph_drawer import graph_drawer
logging.basicConfig(level=logging.WARNING)


def days_infected_checker(infection: infection_graph,p_r: float, fatal_days: int = 10 ) -> None:
    """This function checks how long the node has been infected for so the node can either die or recover

    Args:
        infection (infection_graph): The graph were studying
        p_r (float): The reocvery rate from the model
        fatal_days (int, optional): The number of days it takes for the virus to either kill someone or recover. Defaults to 10.
    """    
    for node in infection.daysinfected: 
            if node in infection.infected: #if its infected add 1 to its days infected
                infection.daysinfected[node] += 1
            if infection.daysinfected[node] > fatal_days: #if the daysinfected is greater than fatal days then it will either die or recover
                infection.die_or_recover(node,p_r)
    
def model(graph: nx.Graph,p_i: float, p_r: float,intial_infected: int = 1,intial_immune: int = 0,enable_vis: bool = False,infection_type: infection_strat = ConstantRateInfection,graph_type: str = 'Not Defined') -> tuple[dict,dict]:
    """The main SIRD model

    Args:
        graph (nx.Graph): The input graph which the model will run on
        p_i (float): Probaility of infection
        p_r (float): Probability of recovery
        intial_infected (int, optional): Number of intial infected people. Defaults to 1.
        intial_immune (int, optional): Number of intially immune people. Defaults to 0.
        enable_vis (bool, optional): Decides wether to show a visualisation of the graph. Defaults to False.
        infection_type (infection_strat, optional): The infection strategy. Defaults to ConstantRateInfection.
        graph_type (str, optional): The type of graph were using. Defaults to 'Not Defined'.

    Raises:
        Exception: If the model is not running correctly. we will raise an error

    Returns:
        tuple[dict,dict]: The tuple contains information about the graph, the infection parameters and data from the model
    """    
    infection_network = infection_graph(graph.copy(),initial_infected=intial_infected,intial_immune = intial_immune,enable_vis=enable_vis) #Creates an instance of the infection_graph
    origin_network = deepcopy(infection_network) #Makes a copy of G so we can compare later
    days_of_the_infcetion = 0
    '''For all intensive purposes this for loop will run forever until either all the nodes die or the infection dies out'''
    for _ in range(100000):
        infection_type.infect(infection_network,p_i) #We call the infect func on our graph and we will do this many times
        '''Here we look in daysinfected and increment the time a node has been infected by one then see if any node has been
        infected for more than 10 days if so the node will attempt to recover or die'''
        days_infected_checker(infection_network,p_r,2)
        '''If there is no nodes left infected either everyones dead or everyones recovered''' 
        if len(infection_network.infected) == 0:
            '''If theres no nodes left in the graph everyones dead'''
            if infection_network.vertices == []:
                no_of_survivors = 0 #Everyones dead, no survivors
                total_death = True
                if enable_vis is True:
                    '''We render the plot of the orginal graph to see how it looked and maybe why everyone died,
                    theres no point showing the final graph as itll just be empty'''
                    f = plt.figure('Staring graph')
                    #subax1 = plt.subplot(121)
                    nx.draw(origin_network.nxgraph,node_color = origin_network.colours.values(),with_labels=True)
                    f.show()
                    input()
            else:
                '''Otherwise if people did survive then we make a list of everyone who survived'''
                no_of_survivors = len(infection_network.vertices)
                total_death = False
                if enable_vis is True:
                    '''Here we render both the orginal grpah and a graph of all the survivors to compare the devasation or lack there of'''
                    print(infection_network.colours)
                    infection_network.update_picture()
                    print(infection_network.colours)
                    f = plt.figure('Starting Graph')
                    nx.draw_networkx(origin_network.nxgraph,node_color = origin_network.colours.values() ,pos=origin_network.pos,with_labels=True)
                    f.show()
                    g = plt.figure('The survivors')
                    nx.draw(infection_network.nxgraph,node_color = infection_network.colours.values(),pos=infection_network.pos,with_labels=True)
                    g.show()
                    input()
            
            '''Returns a lot of useful info about the graph'''
            infection_info = {'n':origin_network.no_nodes,
                              'e': origin_network.edges,
                              'P_i': p_i,
                              'P_r': p_r,
                              'Days_Taken': days_of_the_infcetion,
                              'survivors': no_of_survivors,
                              'Everyone_Dead':total_death,
                              'Infection_Type': infection_type.__str__(),
                              'Graph_Type':graph_type} | infection_network.inf_stats()
            return infection_info,origin_network.stats()     
        #Increments the time the infcetions been going on for
        days_of_the_infcetion += 1
    else:
        err = "The model failed to complete for unforseen reasons"
        raise Exception(err)

    
def main():
    #result = model(*userpanel())
    g = graph_drawer.generate_random_graph(25,0.2)
    result = model(g,0.6,0.2,enable_vis=True)
    output_window(result)
    # testing = [100,200,300,500,600,700,800,900,1000,1500,2000,2500,3000,4000,5000,6000,7000]
    # times = []
    # for i in testing:
    #     time = perf_counter()
    #     graph = generate_random_graph(i,0.2)
    #     print(model(graph,0.6,0.3))
    #     time_taken = perf_counter()-time
    #     times.append(time_taken)
    # print(times)
    
    
    
    
if __name__ == '__main__':
    main()
   
    


















