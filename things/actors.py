class actor:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.score = 0
        self.prev_msgs = []
        self.num_questions = 0

    def update_score(self, correct):
        if correct:
            self.score += 1
        self.num_questions += 1

    def save_msg(self, msg):
        self.prev_msgs.append(msg)

    def reset(self):
        self.score = 0
        self.prev_msgs = []

