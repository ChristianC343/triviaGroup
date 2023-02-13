leaderboard = []

def save_user(name, score):
    print("I am saving your information!")
    user = {"name": name, "score": score}
    leaderboard.append(user)

def writefile(file_name):
    print("I am adding your information to the leaderboard")
    user_exists = False
    with open(file_name, "a") as file:
        for user in leaderboard:
            found = False
            for existing_user in leaderboard:
                if user["name"] == existing_user["name"]:
                    existing_user["score"] = int(existing_user["score"]) + int(user["score"])
                    found = True
                    break

        if not user_exists:
            line = "{}, {}\n".format(user["name"], user["score"])
            file.write(line)


def get_user(name):
    for user in leaderboard:
        if user["name"] == name:
            return True
    return False
