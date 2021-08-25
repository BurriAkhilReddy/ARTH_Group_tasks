## **Using Application**
---
- Install the required software and packages base on your machine and use the following command
    
    ```
    python3 menu.py
    ```
## **Installation:**
---
### **Windows:**
- Windows users can directly use the application after installing the software under prerequisites section using the command python3 [menu.py](./menu.py)
### **Linux:**
- Linux users need to run the [install.sh](./install.sh) script which will create an user with the required permissions

## **Working:**
---
### **Windows:**
- On windows only the remote and the aws options would work
### **Linux:**
- `RedHat` : All menus will work on RedHat but prerequisites must be installed if they are not installed during execution they give error for the option that uses that tool. It works the same on `CentOS` and `Fedora` too.
- Other linux flavours have some compatible option.

## **Prerequisite:**
---
### **Softwares:**
#### **Linux:**
- `httpd`
- `espeak-ng`
- `python3`
- `awscli`
- These softwares can be installed on linux using the [install.sh](install.sh) script

#### **Windows:**
- `python3`
- `awscli`
### **Python packages:**
- `pyttsx3`
- `boto`
- `boto3`

## **About Application**
---
A cli-menu application which does the configuration of the stuff that we do in linux, docker, hadoop and aws easy and faster. It has three work spaces which are local workspace, remote workspace, and aws workspace based on the requirement one needs to choose one of the workspace and use the menus provided by them respectively. As we need do configuration of the tools in many places we can automate this configuration to make the work of the user simpler. This program is built to make the configuration steps easier to the user. This program use the ssh(secure shell), scp(secure copy) and aws-cli in background to do the task in the options of the program. To integrate them together I have used python.

This program will work with the remote as RedHat OS and local host as both windows and RedHat OS 

Even you can work on the remote user and launch instances, create volumes, use cloud front AWS workspace and many more operations can be performed using the program.