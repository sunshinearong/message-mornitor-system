
import unittest
from constants import *
import agent

# --- tests --------------------------------------------------------------

class TestAgent(unittest.TestCase):

    def test_constructor(self):
        """Tests construction of an agent object."""
        try:
            a = agent.Agent(PersonalityType.CHATTY)
        except:
            self.fail("Could not create an Agent object.")

    def test_get_personality(self):
        """Tests the an agent object can be constructed and will return
        the correct personality type when queried."""

        try:
            a = agent.Agent(PersonalityType.CHATTY)
            self.assertEqual(a.get_personality(), PersonalityType.CHATTY)

            b = agent.Agent(PersonalityType.QUIET)
            self.assertEqual(b.get_personality(), PersonalityType.QUIET)
        except:
            self.fail("Could not create an Agent object or run get_personality member function.")

    def test_receive_message(self):
        """Tests that the receive_message method has been written."""

        try:
            a = agent.Agent(PersonalityType.CHATTY)
            a.receive_message(0, 0, MessageType.RED)
            a.receive_message(0, 1, MessageType.GREEN)
            a.receive_message(0, 2, MessageType.BLUE)
        except:
            self.fail("Could not call Agent receive_message method.")

    def test_broadcast_new_message(self):
        """Tests that the broadcast_new_message method has been written. Note that
        this test is statistical and may fail in rare instances."""

        try:
            a = agent.Agent(PersonalityType.CHATTY)
        except:
            self.fail("Could not create an Agent object.")
        
        num_trials = 10000
        msg_freq = [0, 0, 0]
        for i in range(num_trials):
            msg_type = a.broadcast_new_message()
            self.assertTrue(msg_type is None or isinstance(msg_type, MessageType))
            if msg_type is not None:
                msg_freq[msg_type] += 1

        msg_freq = list(map(lambda x: float(x) / num_trials, msg_freq))
        self.assertAlmostEqual(msg_freq[0], 0.3, 1)
        self.assertAlmostEqual(msg_freq[1], 0.1, 1)
        self.assertAlmostEqual(msg_freq[2], 0.2, 1)

    def test_forward_message(self):
        """Tests that the forward_message method has been written. Note that
        this test is statistical and may fail in rare instances."""

        try:
            a = agent.Agent(PersonalityType.CHATTY)
        except:
            self.fail("Could not create an Agent object.")

        num_trials = 10000
        send_freq = [0, 0]
        for msg_id in range(num_trials):
            a.receive_message(0, msg_id, MessageType.RED)
            self.assertFalse(a.forward_message(0, PersonalityType.QUIET, msg_id, MessageType.RED))
            send = a.forward_message(1, PersonalityType.QUIET, msg_id, MessageType.RED)
            if send:
                send_freq[0] += 1
            else:
                send_freq[1] += 1

        send_freq = list(map(lambda x: float(x) / num_trials, send_freq))
        self.assertAlmostEqual(send_freq[0], 0.3, 1)




if __name__ == '__main__':
    unittest.main()
