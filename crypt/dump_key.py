import bcrypt
import pickle
import platform

miala = "$2b$12$756DDkcwBZ5haPlodjJLP."

print(len(miala))
def save_object(obj, object_name):
    with open(object_name, "wb") as file:
        my_depickler = pickle.Pickler(file)
        my_depickler.dump(obj)

def load_object(object_name):
    with open(object_name, "rb") as file:
        my_depickler = pickle.Unpickler(file)
        data = my_depickler.load()
    return data

# save_object(bcrypt.gensalt(),"salt")
salt = load_object("salt")

name = platform.uname().node

name = "ddsfqgqhfdk"
mdp = bcrypt.hashpw(name.encode('utf-8'),salt).decode("utf-8")[29:]

print(mdp)

#print(len(mdp))
