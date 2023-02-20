class actor:
    def __init__(self, phone_number):
        self.phone = phone_number
        self.prev_msgs = []
        self.state = {"init_flag": True}  # initialize the state dictionary with the "init_flag" variable set to True
        self.waiting = False

    def save_msg(self, msg):
        self.prev_msgs.append(msg)
