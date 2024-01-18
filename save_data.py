import json
from datetime import datetime

def saveData(data):
    # Save data in json file
    title = str(datetime.now())
    title = title.split(".")[0]
    title = title.replace(" ", "_").replace(":", "-")
    with open(str(title) + ".json", "w") as file:
        file.write(json.dumps(data))



def loadData(name):
    # Load previous run from json file
    with open(name, "r") as file:
        content = json.load(file)

    return content



if __name__ == "__main__":
    saveData({"test": "tester"})