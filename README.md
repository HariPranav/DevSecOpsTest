# Effortless Deployment: Building a DevOps Pipeline with Jenkins and Github Actions for Dockerized Flask Apps on Digital Ocean

In this blog, we'll develop a Flask application, create a Docker image, and deploy it using a CI/CD pipeline with Jenkins, Github, and Digital Ocean. This enables efficient collaboration and testing before deploying the latest changes automatically whenever new code is pushed to Git. In future blogs, we'll evolve this DevOps pipeline into a DevSecOps pipeline, integrating SAST and DAST tools at different stages of the development process to check code comprehensively throughout the cycle.


## Create an account on Digital Ocean !

Digital Ocean is a great cloud provider for students, as they offer 200$ worth of free credits when students register with a Github student account which can be activated from the link below. Following the link, we can create a new project and then deploy a Droplet with 1 GB of RAM and 25 GB storage, which is the minimum capacity option available. This instance can be used to perform most of our tasks for the blog.

[Digital Ocean Credits](https://www.digitalocean.com/github-students)

[Digital Ocean Droplet Creation](https://docs.digitalocean.com/products/droplets/how-to/create/#:~:text=You%20can%20create%20one%20from,open%20the%20Droplet%20create%20page.)


Once we have set up the droplet, we can SSH into it or we can access the instance from our console and run the following commands:

```
apt update

apt install openjdk-11-jre
```

## Install Jenkins:

We can refer the link below to install Jenkins

[Installing Jenkins](https://www.jenkins.io/doc/book/installing/linux/)

```
sudo wget -O /usr/share/keyrings/jenkins-keyring.asc \
https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
/etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt-get update

sudo apt-get install jenkins
```

## Install Java as Jenkins requires Java to run

```
sudo apt update
sudo apt install fontconfig openjdk-17-jre
java -version
```

## Start jenkins when the system boots:

```
sudo systemctl enable jenkins
```

![Installing Jenkins](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Installing%20Jenkins.png?raw=true)

## Starting Jenkins :

```
sudo systemctl start jenkins

```

![Accessing Jenkins](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/AccessingJenkinsServer.png?raw=true)

Install the default plugins once logged in 

![Install_Plugins_Jenkins](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Install_Plugins_Jenkins.png?raw=true)

## Dockerizing a Flask application to run using Jenkins

### Installing Docker on the server 

```
sudo apt install docker.io
```

### Next, we can create a Flask application and install the required dependencies as shown:

```
mkdir FlaskApp

cd FlaskApp

# Create a virtual environment

python3 -m venv venv 

# Activate the environment 

source venv/bin/activate

# Install Flask:

pip install Flask

# Create two files : app.py and Dockerfile

touch app.py

touch Dockerfile

```

![Folderstructure_Flask](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/FolderStructure_Flask.png?raw=true)

### Creating a flask application to display a message 

Inside the app.py file we need to paste the code as given below : 

```
from flask import Flask
helloworld = Flask(__name__)
@helloworld.route ("/")
def run ():
    return "{\"message\":\"Hey there Python\"}"

if __name__ == "__main__":
    helloworld.run(host="0.0.0.0", port=int("3000"), debug= True)

```

Inside the Dockerfile we need to paste the code as given below: 

```
FROM python:3-alpine3.15
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./app.py

```

We then create a requirements.txt file and then input flask as given below.

```
mkdir requirements.txt

nano requirements.txt

flask

```

Next we can build the container and run it 

```
docker build -t hari1 .

docker run -d -p 3000:3000 hari1

```

If all the steps work, then we can access our flask application inside the docker container as given in the screenshot below : 

![Docker_install_successful](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Dockerinstall_Successful.png?raw=true)

If this page does not load up then we need to make sure that the ports are open, this can be troubleshooted as given below: 

[Open ports on Linux](https://www.digitalocean.com/community/tutorials/opening-a-port-on-linux)

## Pushing Code to Github

We can now push our code to git by following the steps given below, in our droplet, let us configure git and login, then create a repository and push the folder with our flask project:

[Pushing a local repo to git repo](https://superuser.com/questions/1412078/bring-a-local-folder-to-remote-git-repo)

Create an empty repository in github, do not check the Add a README option:

![Empty_Git_Repo](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Empty_Git_Repo.png?raw=true)

Then we need to go inside our directory, initialize the git repo, git add all the files and then push the changes to our remote repository highlighted above.

```
cd Flaskapp
```
Then follow the commands as given in the screenshot below. 

```
  git init
  git add README.md
  git commit -m "first commit"
  git branch -M master
  git remote add origin https://github.com/HariPranav/Jenkins_DevSec_Ops.git
  git push -u origin master
```

![Pushing Code to git](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Pushing_Git_Changes.png?raw=true)

When pushing the changes to the repo, we may get errors when we use our github password when prompted as given below,

![Accesstokens_error](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Accesstokens_error%20.png?raw=true)

[Accessing GitHub Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

Hence we need to create access tokens and input that as the password. In our personal github go to **Accounts** -> **Settings** -> SCROLL DOWN TO THE BOTTOM ->  **Developer Settings** -> **Personal Access Tokens** -> **Tokens (classic)** and generate this, when prompted for the password again input these details as shown below , select all the permissions and create tokens 

![Github_Authentication_tokens](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Github_Authentication_tokens.png?raw=true)
 
![Pushing_All_Code_To_Git](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Pushing_All_Code_To_Git.png?raw=true)

## Connecting the Jenkins pipeline to Github 

We can run the ssh-keygen command in the Digital Ocean Droplet to get the public and private keys as shown in the screenshot below

```
ssh-keygen 
```

![Generating SSH keys](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Generating_SSH_Keys.png?raw=true)

Next we need to connect our application to Github, login to github and go to **settings** then go to **SSH and GPG** and paste the **public key (key ending with .pub)** 

![SSH_key_github](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/SSH_Keys_Github.png?raw=true)


## Building CI/CD automation:

Open the Jenkins dashboard and then go to Create a new Item as given in the screenshot below, add a name and then choose **Freestyle project**


![Creating_FirstPipeline_jenkins](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Creating_Firstpipleline_Jenkins.png?raw=true)

Next in the **Configuration Page** give a name to the project, then switch back to github get the project URL and Enable the **Github Project** checkbox and paste the data into it.

![Github_Project_URL](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Github_Project_URL.png?raw=true)

Adding Github Credentials to Jenkins Pipeline

![Adding_Credentials_Jenkins](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Adding_Credentials_Jenkins.png?raw=true)

Select the **ADD** option and select the **SSH Username with private key option**  as shown in the screenshot below:

![Adding_Credentials_Jenkins_Part2](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Adding_Credentials_Jenkins_Part2.png?raw=true)

Scroll down and choose the **Private Key and Enter key directly option**

![AddingPrivateKey](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/AddingPrivateKey.png?raw=true)

Go back to the droplet and in the screenshot below we need to access the **private keys** when generating the keys, we get two of them in the screenshot below we can see **hari and hari.pub**, the key named **hari** is the private key which should not be revealed !. 

Type the following in the terminal to reveal the keys

```
sudo cat hari
```

![PrivateKeys](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/PrivateKeys.png?raw=true)

Next check the **GitHub hook trigger** and the **Delete workspace option** and in the **Build Steps** click on **Execute Shell** as shown below:

![BuildSteps_Triggers](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/BuildSteps_Triggers.png?raw=true)

Then Paste the code as given below:

```
docker build -t hari1 .

docker run -d -p 3000:3000 hari1
```

Next to detect changes for every github change, we need to specify the jenkins url to github which uses it as a webhook.

Go to github, go to the repository -> settings, web hooks and add the jenkins repository.

![Addingwebhooks](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Addingwebhooks.png?raw=true)

The webhook must be in the format : 

```
<public dns address>:8080/github-webhook/
```

Where the public DNS address is the IP of the Digital ocean droplet

Now make a change in the **app.py** and push the changes to git, this should trigger the Jenkins build and this should push the latest version of the application.

We will most probably get an error, which is the docker daemon is not given the permissions to allow the Jenkins user to run the container. Hence we need to explicitly give permissions for the docker container to run the daemon as given below, open the Droplet and add the following command: 

```
sudo usermod -a -G docker jenkins
```

This will allow the Jenkins user to get the necessary permissions to run the docker container. 

In the screenshot below we can see that the changes have been successfully pushed and the container with the flask application with the latest changes are reflected in the web application URL !!!.

![Successfully_Pushed_Code](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/Successfully_Pushed_Code.png?raw=true)

![NewChanges_Reflected](https://github.com/HariPranav/Compliance_In_The_Cloud/blob/master/images/Jenkins_Flask_Digital_Ocean/NewChanges_Reflected.png?raw=true)



References:

https://shravani10k.hashnode.dev/setting-up-jenkins-cicd-pipeline-and-deploying-flask-application-to-aws-ec2

https://www.digitalocean.com/community/tutorials/opening-a-port-on-linux

https://www.jenkins.io/doc/book/installing/linux/
