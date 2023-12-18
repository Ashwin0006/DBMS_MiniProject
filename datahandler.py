import pickle



class Mentor:
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.role = "Mentor"

data = []
m1 = Mentor("Ash", 123)
data.append(m1)
with open(r"data/mentor.pickle", 'wb') as outfile:
    pickle.dump(data, outfile)

with open(r"data/mentor.pickle", 'rb') as outfile:
    data = pickle.load(outfile)
    print(data)
