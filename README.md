
## Overview
 Understanding the dynamics of social
networks such as Facebook and twitter is an important research topic
with many applications including improving online experience
(personalised advertising and search), optimising network bandwidth
(pre-delivery of content), tracking world events (social media),
etc. The same techniques can be applied to modelling networks in the
physical world, such as traffic flows, communication networks, and
disease transmission.

One way to simulate social networks (and physical) is via agent based
modelling. In such a model many agents are programmed with their own
simple rules. 
We will assume
that our social network consists of a number of users (agents), who
interact by sending messages to each other.

- Each user has a fixed set of friends and can only send messages to
  users in this set. The entire social network is modelled by a
  graph. A user is represented by a node in the graph, and edges
  between nodes indicate friendship relations.

- If user _A_ is friends with user _B_ then user _B_ is also friends
  with user _A_ (in the language of graph theory we say that the
  social network is undirected).

- Each user has a personality type, which can be **CHATTY** or
  **QUIET**. The personality type controls how frequenty a user sends
  new messages or forwards old messages.

- Users can only send message to adjacent nodes in the graph, i.e.,
  their friends.

- Messages have an id and a content type---we do not care about the
  exact content of the message, only its type. There are three
  content types: Recreational (**RED**), Gossip (**GREEN**), and
  Business (**BLUE**).

- The simulation proceeds in a series of epochs:

  - At each iteration a user can choose to broadcast a new message to
    all of its friends. A user can only broadcast one new message per
    epoch.

  - At each iteration a user can choose to send (forward) a previously
    received message to one or more of its friends. Multiple different
    messages can be forwarded within an epoch.
    
- A user may receive multiple copies of the same message (identified
  by the message id). However, a user should never send a message back
  to the same friend who sent the message.

- A user should never send the same message to the same friend twice.

- The user's decision to send a new message and the message's content
  type is a random decision governed by the user's personality type.

- The user's decision to forward a message is a random decision
  governed by (i) the user's personality type, (ii) the friend's
  personality type, and (iii) the message's content type.

- A user can only forward a message within the same epoch in which
  the message was received.

- Messages are delivered one epoch after they are sent.



