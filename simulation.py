

import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from constants import *
import agent
import engine



social_network_structure = 1

# --- drawing functions -----------------------------------------------------

def draw_social_network(e, positions):
    """Draws the social network on the current plot."""
    plt.cla()
    plt.axis('off')
    nx.draw_networkx_edges(e.graph, positions, edge_color="#ffffff", width=5, alpha=0.5)
    for node in e.graph:
        nx.draw_networkx_nodes(e.graph, positions, nodelist=[node],
            node_color=e.get_node_colour(node), node_shape=e.get_node_shape(node), node_size=500)
    nx.draw_networkx_labels(e.graph, positions)
    plt.title("Social Network (epoch {})".format(e.num_epochs))

def draw_agent_statistics(e):
    """Draws bar graph of messages sent by each agent on the current plot."""
    plt.cla()
    r, g, b = e.get_message_counts_by_node()
    indx = np.arange(e.num_agents())
    width = 0.65

    plt.bar(indx, r, width, color="#ff7f7f")
    plt.bar(indx, g, width, bottom=r, color="#7fff7f")
    plt.bar(indx, b, width, bottom=r+g, color="#7f7fff")

    plt.xticks(indx + width/2, indx)
    plt.legend(labels=("Recreational", "Gossip", "Business"))
    plt.title("Messages Sent by Agent per Type")
    plt.xlabel("Agent Id")
    plt.ylabel("Cumulative Number of Messages")

def draw_message_statistics(e):
    """Draws messages statistics per epoch on the current plot."""
    plt.cla()

    r, g, b = e.get_message_counts_by_epoch()
    indx = np.arange(e.num_epochs) + 1

    r, g, b = plt.plot(indx, r, indx, g, indx, b, linewidth=2)
    plt.setp(r, color="#ff7f7f")
    plt.setp(g, color="#7fff7f")
    plt.setp(b, color="#7f7fff")

    plt.title("Messages Sent per Epoch by Type")
    plt.xlabel("Epoch")
    plt.ylabel("Number of Messages")

# --- event processing ------------------------------------------------------

def animate_events(fnum, e, positions):
    # draw the social network
    plt.subplot(1, 4, 1)
    draw_social_network(e, positions)

    evt = e.peek_next_event()
    if evt is not None:
        src, dst_list, msg_id, msg_type = evt
        colour = ["#ff0000", "#00ff00", "#0000ff"][msg_type]
        for dst in dst_list:
            nx.draw_networkx_edges(e.graph, positions, edgelist=[(src, dst)], edge_color=colour, width=3)

        nx.draw_networkx_nodes(e.graph, positions, nodelist=[src],
            node_color=e.get_node_colour(src), node_shape=e.get_node_shape(src), node_size=700)

    # draw the agents states
    plt.subplot(1, 4, 2)
    draw_agent_statistics(e)

    # draw the message statistics
    if evt is None:
        plt.subplot(1, 4, 3)
        if e.num_epochs > 1:
            draw_message_statistics(e)
        else:
            plt.axis('off')
            plt.text(0.5, 0.5, "waiting for 2 epochs...", horizontalalignment='center', fontsize=12)
    # process the next event
    plt.subplot(1,4,4)  #plot message longity in the fourth subplot
    plt.cla()
    width=0.65
    plt.bar(np.arange(3),np.array(e.msg_type_id)*1.000/e.num_epochs,width)  #(sum of message) / time
    plt.xticks(np.arange(3) + width / 2,np.arange(3))
    plt.title("Messages longity")
    plt.xlabel("Message type")
    plt.ylabel("longity")
    e.process_event()

# --- graph creation --------------------------------------------------------

def create_random_graph():
    #e = engine.Engine(nx.connected_caveman_graph(5, 4))
    #e = engine.Engine(nx.fast_gnp_random_graph(20, 0.2))
    e = engine.Engine(nx.watts_strogatz_graph(20, 5, 0.2))
    return e

def create_chatty_ring(n = 6):
    g = nx.Graph()
    for a in range(n):
        g.add_node(a)
    for a in range(n):
        g.add_edge(a, (a + 1) % n)

    return engine.Engine(g, 1.0)

def create_quiet_ring(n = 6):
    g = nx.Graph()
    for a in range(n):
        g.add_node(a)
    for a in range(n):
        g.add_edge(a, (a + 1) % n)

    return engine.Engine(g, 0.0)

def create_mixed_ring(n = 6):
    g = nx.Graph()
    for a in range(n):
        g.add_node(a)
    for a in range(n):
        g.add_edge(a, (a + 1) % n)

    return engine.Engine(g, personalities={a: a % 2 for a in range(n)})

def create_segregated_ring(n = 6):
    g = nx.Graph()
    for a in range(n):
        g.add_node(a)
    for a in range(n):
        g.add_edge(a, (a + 1) % n)

    return engine.Engine(g, personalities={a: 0 if a < n/2 else 1 for a in range(n)})
# def Message_longity(e):
#     r,g,b=e.get_message_counts_by_epoch
#     e.num_epochs

# --- main ------------------------------------------------------------------

if __name__ == "__main__":

    # construct the social network
    if (social_network_structure < 1) or (social_network_structure > 5):
        social_network_structure = random.randint(1, 5)

    if social_network_structure == 1:
        e = create_chatty_ring()
    elif social_network_structure == 2:
        e = create_quiet_ring()
    elif social_network_structure == 3:
        e = create_mixed_ring()
    elif social_network_structure == 4:
        e = create_segregated_ring()
    elif social_network_structure == 5:
        e = create_random_graph()

    # set up visualisation
    plt.ioff()                                  # turn off interactive mode
    fig = plt.figure()                          # intialize the figure
    positions = nx.spring_layout(e.graph)       # determine fixed node positions
    # start the animation
    plt.subplot(1, 3, 1)
    draw_social_network(e, positions)
    ani = animation.FuncAnimation(fig, animate_events, interval=30, repeat=False, fargs=(e, positions), frames=1000)
    plt.show()
