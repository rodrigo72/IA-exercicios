class Node:
    def __init__(self, name, id=-1):
        self.m_id = id
        self.m_name = str(name)

    def __str__(self):
        return "node " + self.m_name

    def set_id(self, id):
        self.m_id = id

    def get_id(self):
        return self.m_id

    def get_name(self):
        return self.m_name

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.m_name == other.get_name()
        return False

    def __hash__(self):
        return hash(self.m_name)
