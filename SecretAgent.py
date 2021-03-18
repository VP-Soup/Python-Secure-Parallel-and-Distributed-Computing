"""
Name: Vicente James Perez
Date: 1/16/2020
Assignment: Module 2: Secret Agent Class
Due Date: 1/17/2020
About this project: Create a class with specified member vars and a script that prints each member
Assumptions:NA
All work below was performed by Vicente James Perez
"""


class SecretAgent(object):
    # initializer function takes 4 inputs to create the 4 member variables
    def __init__(self, agent_id, agent_name, agent_alias, agent_security_level):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.agent_alias = agent_alias
        self.agent_security_level = agent_security_level

    # function to override print() for objects of this class - prints all member vars in different lines.
    def __str__(self):
        return (f'AgentID: {self.agent_id}\nAgentName: {self.agent_name}\nAgentAlias: {self.agent_alias}\n'
                f'AgentSecurityLevel: {self.agent_security_level}\n')

    # was going to add mutators and accessors but saw the discussion board question


# creates 3 instances of SecretAgent Class and prints each.
agent1 = SecretAgent(1, 'Vicente', '001', 1)
agent2 = SecretAgent(2, 'James', '002', 2)
agent3 = SecretAgent(3, 'Perez', '003', 3)
print('Agent1:')
print(agent1)
print('Agent2:')
print(agent2)
print('Agent3:')
print(agent3)


