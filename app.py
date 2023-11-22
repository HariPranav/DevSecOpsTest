from flask import Flask
helloworld = Flask(__name__)
@helloworld.route ("/")
def run ():
    return "{\"message\":\"Success, The latest changes have been triggered, we need to add the jenkins user to docker to give it permissions to run !!!!!! \"}"

if __name__ == "__main__":
    helloworld.run(host="0.0.0.0", port=int("3000"), debug= True)
