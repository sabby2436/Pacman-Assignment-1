# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):

        # checking if a state is Win or Lose state, if yes terminating the game
        if state.isWin() or state.isLose():
            return Directions.STOP
            
        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action, 1) for action in legal]
        
            
        #Array for maintaining best     
        min_score =[]
        best_action =[]		

        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action, 1) for action in legal]
        #print('succs',successors)
        flag = True

        while successors:
            # taking first element out of the sorted array, since we are maintaing queue ie FIFO 
            #and hence popping the first element and later on we will append this value in successor
            successor = successors.pop(0)
            #print('successor', successor)
			
            if successor[0] is not None:
					
				#Checking whether it's not in isLose	
				if successor[0].isLose():
					continue
				
				#if it's the first element, store the best action and 	
				if flag:
					best_action = successor[1]
					#print('action' , best_action)
					min_score = admissibleHeuristic(successor[0]) + successor[2]
					#print('score' , min_score)
					flag = False
					
				#function to maintain and return child action and child score and return them	
				def child (i,j,k):
					c_actions = i.getLegalPacmanActions()
					#print('actions', c_actions)
					c_score = []
					child1=[]
					
					for x in c_actions:
						s = ++k
						child1 = (i.generatePacmanSuccessor(x),j, s)
					
					if child1[0] is not None :
						if not child1[0].isLose():
							successors.append(child1) #Appending child1 scores to successors
							c = admissibleHeuristic(child1[0]) + child1[2]
							c_score.append(c)	
						
					return c_score
									
				c_score = child(successor[0],successor[1],successor[2])
				
				
				#Check for the best action array and best score
				if best_action is not None:
					if min_score is not None:
						if successor[0] is not None or len(c_score) is not None:
							if successor[0] is not None and successor[1] is not None and successor[2] is not None:
								s_score = admissibleHeuristic(successor[0]) + successor[2]
								if s_score < min_score:
									best_action = successor[1]
									min_score = s_score
								
								elif c_score is not None and len(c_score) > 0:
									if(successor[1] is None):
										return
									else:
										final_score = min(c_score)
										if final_score<min_score:
											best_action = successor[1]
											min_score = final_score

										
				#returning the final action
				final_action = best_action
				print('best action', final_action)
				return final_action
				
							
										


class DFSAgent(Agent):
    
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):

        # checking if a state is Win or Lose state, if yes terminating the game
        if state.isWin() or state.isLose():
            return Directions.STOP

        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action, 1) for action in legal]
        
        #Taking 2 1D array for maintaing best action and best score
        best_action =[]
        min_score =[]

        while successors:
			
			# we are popping out the last element because according to DFS algo we maintain a stack
			#Since stack works on LIFO procedure we will 
            successor = successors.pop()
            #print( 'state' , successor)
            
            if successor[0] is not None:
				
				flag = True
					
				if successor[0].isLose():
					continue
				
				#if the first element, initialize with best score and best action	
				if flag:
					best_action = successor[1]
					#print ('action', best_action)
					min_score = admissibleHeuristic(successor[0]) + successor[2]
					#print('score', min_score)
					

				
				#function to maintain and return child action and child score and return them
				def child(i,j,k):
					c_actions = i.getLegalPacmanActions()
					print('child actions', c_actions)
					child1 = []
					c_score = []
					
					for x in c_actions:
						s = k
						child1 = (i.generatePacmanSuccessor(x), j, ++s)
						
						if child1[0] is None:
							return
						else:
							if not child1[0].isLose():
								successors.append(child1) #appending child1 scores to successor
								c = admissibleHeuristic(child1[0]) + child1[2]
								c_score.append(c)
				 
				
				
				
				c_score = child(successor[0], successor[1], successor[2])
				
				
				#Check for the best action array and best score
				if best_action is not None:
					if min_score is not None:
						if c_score is not None and len(c_score)>0:
							if successor[0] is not None and successor[1] is not None and successor[2] is not None:
								s_score = admissibleHeuristic(successor[0]) + successor[2]
								if s_score < min_score:
									best_action = successor[1]
									min_score = s_score
									
									
							elif len(c_score) > 0:
								if successor[1] is not None:
									best_score = min(c_score)
									if best_score < min_score:
										best_action = successor[1]
										min_score = best_score
										
				final_action = best_action
				print('final action', final_action)
				return final_action						
											


class AStarAgent(Agent):

    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):

        # checking if a state is Win or Lose state, if yes terminating the game
        if state.isWin() or state.isLose():
            return Directions.STOP

        legal = state.getLegalPacmanActions()
        successors = [(state.generatePacmanSuccessor(action), action, 1) for action in legal]
        
        # Taking two 1D array for maintaing best action and best scores
        best_action = []
        best_score = []

        flag = True

        for successor in successors:

            # for sorting the array of elements since Astar works on the basis of scores
            if len(successors) > 1:
                successors.sort(key=lambda x: (admissibleHeuristic(successor[0])+successor[2]))

            # taking first element out of the sorted array
            successor = successors.pop(0)

            if successor[0] is not None:

                if successor[0].isLose():
                    continue

                if flag:
                    best_action = successor[1]
                    #print('best action', best_action)
                    best_score = admissibleHeuristic(successor[0]) + successor[2]
                    #print ('best_score', best_score)
                    flag = False

                 #Child Actions 
                c_actions = successor[0].getLegalPacmanActions()
                c_scores = []

                for x in c_actions:
                    child1 = (successor[0].generatePacmanSuccessor(x), successor[1], ++successor[2])

                    if child1[0] is not None and not child1[0].isLose():
                        successors.append(child1) #appending child in successors 
                        c_scores.append(admissibleHeuristic(child1[0]) + child1[2])

                # None check for best action and best scores
                if best_action is not None and best_score is not None:

                    if c_scores is None:
						if len(c_scores) == 0:
							if successor[0] is not None and successor[1] is not None and successor[2] is not None:
								s_score = admissibleHeuristic(successor[0]) + successor[2]
								if s_score < best_score:
									best_action = successor[1]
									best_score = s_score

                    
                    elif c_scores is not None:
						if len(c_scores) > 0:
							if successor[1] is not None:
								min_score = min(c_scores)
								if min_score < best_score:
									best_action = successor[1]
									best_score = min_score

        # returning the final_actions
        final_action = best_action
        print('final action', final_action)
        return final_action


