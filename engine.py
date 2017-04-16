# COMP1040: The Craft of Computing
#
# Engine class for holding the social network graph and managing
# the sending of messages between agents.
#
# ONLY MODIFY CODE IN THIS FILE FOR THE LAST TASK OF THE ASSIGNMENT.
#

from collections import deque
import random
import networkx as nx
import numpy as np

import agent
from constants import *

class Engine(object):

    def __init__(self, graph, pr_chatty = 0.5, personalities = None):
        """Initialises the engine with a graph. Personalities types
        are either randomly assigned or chosen from a dictionary
        of personalities keyed by node identifier.
        """
        self.graph = graph
        self.agents = []
        for node in range(self.graph.number_of_nodes()):
            # check if personalities given
            if (personalities is not None) and (node in personalities):
                self.agents.append(agent.Agent(personalities[node]))
                continue

            # otherwise flip a biased coin
            coin = random.random()
            if  coin < pr_chatty:
                self.agents.append(agent.Agent(PersonalityType.CHATTY))
            else:
                self.agents.append(agent.Agent(PersonalityType.QUIET))

        self.agent_stats = [[0, 0, 0] for a in self.agents]     # clear agent statistics
        self.epoch_stats = []           # number of messages of each type sent each epoch
        self.num_epochs = 0             # initialise number of epochs
        self.msg_counter = 0            # unique message counter
        self.event_queue = deque()      # None or (src_id, [tgt_id], msg_id, msg_type)
        self.msg_type_id=[0,0,0]        #initialise number of each type message [RED sum,GREEN sum,BLUE sum]
    def num_agents(self):
        """Return the number of agents in the network."""
        return len(self.agents)

    def peek_next_event(self):
        """Return the next event to be processed."""
        return self.event_queue[0] if self.event_queue else None

    def process_event(self):
        """Process the next event on the event queue."""

        # Pop next event. An empty queue or the sentinel None indicates
        # the end of an epoch and users may choose to send new messages.
        evt = self.event_queue.popleft() if self.event_queue else None

        if evt is None:
            # intialize next epoch statistics
            self.epoch_stats.append([0, 0, 0])
            self.num_epochs += 1

            # new messages
            for agent_id in self.graph:
                # decide whether to send a message
                msg_type = self.agents[agent_id].broadcast_new_message()
                if msg_type is None: continue

                msg_id = self.msg_counter
                self.msg_counter += 1
                print("Agent {} is broadcasting a message of type {} with id {}.".format(agent_id, msg_type, msg_id))
                self.msg_type_id[msg_type] +=1  #update msg_type_id
                # schedule the messages to be sent to all neighbours
                self.event_queue.append((agent_id, list(self.graph[agent_id]), msg_id, msg_type))

            # trigger next epoch
            self.event_queue.append(None)

        else:
            # deliver messages
            src_id, dst_list, msg_id, msg_type = evt
            for dst_id in dst_list:
                self.agents[dst_id].receive_message(src_id, msg_id, msg_type)

                # update statistics
                self.agent_stats[src_id][msg_type] += 1
                self.epoch_stats[-1][msg_type] += 1

                # decide whether to forward the message to each neighbours
                broadcast_list = []
                for friend_id in self.graph[dst_id]:
                    if self.agents[dst_id].forward_message(friend_id, self.agents[friend_id].get_personality(), msg_id, msg_type):
                        print("Agent {} is forwarding a message of type {} with id {} to friend {}.".format(dst_id, msg_type, msg_id, friend_id))
                        self.msg_type_id[msg_type] += 1 #update msg_type_id
                        broadcast_list.append(friend_id)
                if broadcast_list:
                    # schedule messages to be sent
                    self.event_queue.append((dst_id, broadcast_list, msg_id, msg_type))

    def get_node_colour(self, node):
        """Return the colour of a node based on messages sent."""
        r, g, b = tuple([c + 32 for c in self.agent_stats[node]])
        scale = 255 / max(r, g, b)
        return "#{:02x}{:02x}{:02x}".format(int(scale * r), int(scale * g), int(scale * b))

    def get_node_shape(self, node):
        """Return the shape of a node based on it's personality."""
        return ["o", "s"][self.agents[node].get_personality()]

    def get_node_importance(self, node):
        """Return the importance of a node based on the number of messages sent."""
        return sum([c for c in self.agent_stats[node]])

    def get_message_counts_by_node(self):
        """
        Returns the number of messages of each type sent by each node.

        :return: 3-tuple of arrays, one for each message type. Each array contains
        the number of messages of the corresponding type sent by each agent.
        """

        r = np.array([a[0] for a in self.agent_stats])
        g = np.array([a[1] for a in self.agent_stats])
        b = np.array([a[2] for a in self.agent_stats])

        return (r, g, b)

    def get_message_counts_by_epoch(self):
        """
        Returns the number of messages of each type sent during each epoch.

        :return: 3-tuple of arrays, one for each message type. Each array contains
        the number of messages of the corresponding type sent during each epoch.
        """

        r = np.array([a[0] for a in self.epoch_stats])
        g = np.array([a[1] for a in self.epoch_stats])
        b = np.array([a[2] for a in self.epoch_stats])
        return (r, g, b)

