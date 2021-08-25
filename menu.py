#host operating system WINDOWS or REDHAT

from subprocess import getoutput
import os
import platform
from colorama import Fore,Back,Style
import pyttsx3

#running with the menuprog user
def run_as(cmd):
    if platform.system()=='Window':
        return os.system(cmd)
    elif platform.system()=='Linux':
        cmd=cmd.replace('\'','\\\'').replace('\"','\\\"').replace('$','\$')
        return os.system(f"""echo "{cmd}" | sudo su menuprog""")

#running with the menuprog user
def run_as_(cmd):
    if platform.system()=='Window':
        return os.system(cmd)
    elif platform.system()=='Linux':
        cmd=cmd.replace('\'','\\\'').replace('\"','\\\"').replace('$','\$')
        return getoutput(f"""echo "{cmd}" | sudo su menuprog""")

#defining a function for frequently used command
def remote_command(cmd,ip=None,username=None,keyfile=None):
    cmd=cmd.replace('\'','\\\'').replace('\"','\\\"').replace('$','\$')
    if keyfile is not None:
        return f'ssh -o StrictHostKeychecking=no -i  {username}@{ip} "{cmd}"'
    return f'ssh -o StrictHostKeychecking=no {username}@{ip} "{cmd}"'

def copyid(ip,username,key):
    query = ''
    while 1:
        query = input("Do you want to login with key file(Y/N): ").strip()
        if query == 'Y' or query == 'N':
            break
    if query == 'Y':
        keyfile = input("Enter the path for private key of the remote system(absolute path): ").strip()
        if run_as(f'test -f {keyfile}')==0:
            run_as(remote_command('echo {0} | ls ~/.ssh; if [ $? -ne 0] ;then mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys;else cat >> ~/.ssh/authorized_keys; fi'.format(key),ip,username,keyfile))
        else:
            print("Key file doesn't exist")
    else:
        run_as(remote_command('echo {0} | ls ~/.ssh; if [ $? -ne 0] ;then mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys;else cat >> ~/.ssh/authorized_keys; fi'.format(key),ip,username))

#ssh-keygen to have a good user experience
def ssh_connect(ip,username):

    if platform.system()=='Windows':
        run_as(r"""ssh-keygen -t rsa -N '' -f %homepath%\\.ssh\\id_rsa.pub""")
        f = open('{0}\.ssh\id_rsa.pub'.format(run_as_(r"echo %homepath%")),'r')
        out=f.read()
        return copyid(ip,username,out)
    elif platform.system()=='Linux':
        run_as(r"""ssh-keygen -t rsa -N '' -f $HOME/.ssh/id_rsa.pub""")
        out = run_as_('cat $HOME/.ssh/id_rsa.pub')
        copyid(ip,username,out)
    else:
        print("Program can run only on Windows and Linux machines")

#Configuration file for namenode
#hdfs-site.xml(NAMENODE)
def hdfs_site_name(directory):
    return """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.name.dir</name>
<value>/{}</value>
</property>
</configuration>
""".format(directory)

#Configuration file for datanode
#hdfs-site.xml(DATANODE)
def hdfs_site_data(directory):
    return """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>dfs.data.dir</name>
<value>/{}</value>
</property>
</configuration>
""".format(directory)

#Configuration file for namenode
#core-site.xml(NAMENODE)
def core_site_name():
    return """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://0.0.0.0:9001</value>
</property>
</configuration>
"""


#Configuration file for datanode
#core-site.xml(DATANODE)
def core_site_data(ip):
    return """<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>

<!-- Put site-specific property overrides in this file. -->

<configuration>
<property>
<name>fs.default.name</name>
<value>hdfs://{0}:9001</value>
</property>
</configuration>
""".format(ip)

#function to copy the configuration file into a temporary file config_file.txt
def save(x):
    f = open('config_file.txt','w')
    f.write(x)
    f.close

while 1:
    login = input(Fore.YELLOW+'Where do you want to work (local/remote/aws):'+Style.RESET_ALL)
    if login=='remote':
        ip = input(Fore.YELLOW+"Give the remote system's IP: "+Style.RESET_ALL)
        username = input(Fore.YELLOW+"Give the remote system's username: "+Style.RESET_ALL)
        ssh_connect(ip,username)
        while 1:
            print(Fore.GREEN+"""
            Select one of the following options:
            1   : run date command
            2   : start webserver
            3   : stop webserver
            4   : start docker process
            5   : stop docker process
            6   : list all the docker containers
            7   : list all the available image
            8   : pull a docker image
            9   : launch a container
            10  : stop a container
            11  : stop all containers
            12  : copy a file to a container
            13  : copy file from the container
            14  : logs of the container
            15  : attach to an existing container
            16  : start hadoop namenode
            17  : start hadoop datanode
            18  : start hadoop client node
            19  : create a primary partition
            20  : create a extended partition
            21  : format a partition
            22  : create lvm and integrate with hadoop
            23  : provide elsticity to datanode
            24  : create static partition and format it and mount it
            25  : mount a partition to a directory
            bash: to start bash shell
            exit: To quit the remote host terminal
            """+Style.RESET_ALL)
            cmd=input(Fore.YELLOW+"Give a command: "+Style.RESET_ALL)
            if cmd == '1':
                run_as(remote_command('date',ip,username))
            elif cmd == '2':
                run_as(remote_command('systemctl start httpd;setenforce 0;systemctl stop firewalld',ip,username))
                print("Webserver running on http://{0}:80".format(ip,username))
            elif cmd == '3':
                run_as(remote_command('systemctl stop httpd;setenforce 1;systemctl start firewalld',ip,username))
                print("Webserver stopped which is running on http://0.0.0.0:80")
            elif cmd == '4':
                run_as(remote_command('systemctl start docker;setenforce 0;systemctl stop firewalld',ip,username))
                print("Docker service is started")
            elif cmd == '5':
                run_as(remote_command('systemctl stop docker;setenforce 1;systemctl start firewalld',ip,username))
                print("Docker service is stopped")
            elif cmd == '6':
                run_as(remote_command('docker ps -a',ip,username))
            elif cmd == '7':
                run_as(remote_command('docker image list',ip,username))
            elif cmd == '8':
                image=input(Fore.YELLOW+"Give the image name that u want to download: "+Style.RESET_ALL)
                run_as(remote_command('docker pull {}'.format(image),ip,username))
            elif cmd == '9':
                name=input(Fore.YELLOW+"Give a name to the container: "+Style.RESET_ALL)
                opersys=input(Fore.YELLOW+'Give the name of the operating system that u want to launch: '+Style.RESET_ALL)
                run_as(remote_command('docker run -dit --name {0} {1}'.format(name,opersys),ip,username))
                ask=input(Fore.YELLOW+"Do you want to use the container?(y/n): "+Style.RESET_ALL)
                while 1:
                    if ask=='y':
                        run_as(remote_command('docker attach {0}'.format(name),ip,username))
                        break
                    elif ask=='n':
                        break
                    else:
                        print("Wrong input 'y' and 'n' are consdered as correct inputs")
                        ask=input(Fore.YELLOW+"Do you want to use the container?(y/n): "+Style.RESET_ALL)
            elif cmd=='10':
                name=input(Fore.YELLOW+"Give a name (or) ID of the container: "+Style.RESET_ALL)
                run_as(remote_command('docker rm -f {0}'.format(name),ip,username))
                print("Container {} is stopped".format(name))
            elif cmd=='11':
                run_as(remote_command('docker rm -f `docker ps -aq`',ip,username))
            elif cmd=='12':
                source_path=input(Fore.YELLOW+"Give the source path"+Style.RESET_ALL)
                container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                destination_path=input(Fore.YELLOW+"Give the destination path"+Style.RESET_ALL)
                run_as(remote_command("docker cp {0} {1}:{2}".format(source_path,container,destination_path),ip,username))
            elif cmd=='13':
                container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                source_path=input(Fore.YELLOW+"Give the source path"+Style.RESET_ALL)
                destination_path=input(Fore.YELLOW+"Give the destination path"+Style.RESET_ALL)
                run_as(remote_command("docker cp {0}:{1} {2}".format(container,source_path,destination_path),ip,username))
            elif cmd=='14':
                container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                run_as(remote_command("docker logs {0}".format(container),ip,username))
            elif cmd=="15":
                container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                run_as(remote_command("docker attach {0}".format(container),ip,username))
            elif cmd=='16':
                print("You need to have the VM launched for configuring the namenode")
                print("\nCurrent logged in user will be configured as namenode\n")
                directory=input(Fore.YELLOW+"Give the directory for namenode configuration: "+Style.RESET_ALL)
                check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                print("Creating directory...\n")
                while 1:
                    if check=='y':
                        run_as(remote_command("rm -rf /{0};mkdir /{0}".format(directory),ip,username))
                        break
                    elif check=='n':
                        break
                    else:
                        print("Proper input is not given")
                        check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                if check=='n':
                    continue
                print("\nConfiguring the namenode's hdfs-site.xml file...\n")
                save(hdfs_site_name(directory))
                run_as('scp config_file.txt root@{0}:/etc/hadoop/hdfs-site.xml'.format(ip,username))
                print("\nConfiguring the namenode's core-site.xml file...\n")
                save(core_site_name())
                run_as('scp config_file.txt root@{0}:/etc/hadoop/core-site.xml'.format(ip,username))
                print("Formatting the namenode...\n")
                run_as(remote_command('hadoop namenode -format',ip,username))
                print("Starting the namenode...")
                run_as(remote_command("hadoop-daemon.sh start namenode",ip,username))
            elif cmd=='17':
                print("You need to have the VM launched for configuring the datanode")
                print("\nCurrent logged in user will be configured as datanode\n")
                namenode=input(Fore.YELLOW+"Give the namenode's ip,username address: "+Style.RESET_ALL)
                directory=input(Fore.YELLOW+"Give the directory for datanode configuration: "+Style.RESET_ALL)
                print("The data in this dir will be deleted if it exists")
                check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                while 1:
                    if check=='y':
                        run_as(remote_command("rm -rf /{0};mkdir /{0}".format(directory),ip,username))
                        break
                    elif check=='n':
                        break
                    else:
                        print("Proper input is not given")
                        check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                if check=='n':
                    continue
                print("\nConfiguring the datanode's hdfs-site.xml file...\n")
                save(hdfs_site_data(directory))
                run_as('scp config_file.txt root@{0}:/etc/hadoop/hdfs-site.xml'.format(ip,username))
                print("\nConfiguring the datanode's core-site.xml file...\n")
                save(core_site_data(namenode))
                run_as('scp config_file.txt root@{0}:/etc/hadoop/core-site.xml'.format(ip,username))
                print("Starting the datanode...")
                run_as(remote_command("hadoop-daemon.sh start datanode",ip,username))
            elif cmd=='18':
                namenode=input(Fore.YELLOW+"Give the namenode's ip address: "+Style.RESET_ALL)
                save(core_site_data(namenode))
                run_as('scp config_file.txt root@{0}:/etc/hadoop/core-site.xml'.format(ip,username))
            elif cmd=='19':
                run_as(remote_command("lsblk -o NAME",ip,username))
                print("These are the available volumes and partitions: \n")
                volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                while 1:
                    if check=='y':
                        size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                        print("Checking if you have exceeded the primary partition limit...")
                        primary=int(run_as_(remote_command("lsblk /dev/{} -o TYPE|grep part| wc -l".format(volume),ip,username)))
                        if primary<=2:
                            print("You will be able to create a primary partition")
                            run_as(remote_command('printf n\\\\n\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume),ip,username))
                        else:
                            print("You will be able to create a primary partition but yo will not be able to create partitions further in this disk after that")
                            print("Hence we don't recommend to create a primary partition u can create a logical partition")
                        break
                    elif check=='n':
                        break
                    else:
                        print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                        check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
            elif cmd=='20':
                run_as(remote_command("lsblk -o NAME",ip,username))
                print("These are the available volumes and partitions: \n")
                volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                while 1:
                    if check=='y':
                        size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                        print("You will be able to create a primary partition")
                        run_as(remote_command('printf n\\\\ne\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume),ip,username))
                        break
                    elif check=='n':
                        break
                    else:
                        print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                        check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
            elif cmd=='21':
                run_as(remote_command("lsblk -o NAME",ip,username))
                print("These are the available volumes and partitions: \n")
                partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                format_type=input(Fore.YELLOW+"What format type you want to use: "+Style.RESET_ALL)
                print("Formatting the partition...")
                run_as(remote_command("mkfs.{0} /dev/{1}".format(format_type,partition),ip,username))
                run_as(remote_command("udevadm settle",ip,username))
                print("Formated the partition")
            elif cmd=='22':
                run_as(remote_command("fdisk -l",ip,username))
                print("Creating physical volumes")
                vol1=input(Fore.YELLOW+"Give the name of the first volume"+Style.RESET_ALL)
                vol2=input(Fore.YELLOW+"Give th name of the second volume"+Style.RESET_ALL)
                run_as(remote_command("pvcreate /dev/{}".format(vol1),ip,username))
                run_as(remote_command("pvcreate /dev/{}".format(vol2),ip,username))
                print(Fore.YELLOW+"Combining physical volumes")
                vg=input(Fore.YELLOW+"Give name to volume group: "+Style.RESET_ALL)
                run_as(remote_command("vgcreate {0} /dev/{1} /dev/{2}".format(vg,vol1,vol2),ip,username))
                print("Information of the volume group")
                run_as(remote_command("vgdisplay {vg}".format(vg),ip,username))
                print("Creating logical volumes")
                lv=input(Fore.YELLOW+"Give the logical volume name: "+Style.RESET_ALL)
                size=float(input(Fore.YELLOW+"Give size in GiB of the logical volume you want to create: "+Style.RESET_ALL))
                run_as(remote_command("lvcreate --size {0}G --name {1} {2}".format(size,lv,vg),ip,username))
                print("Information about logical volumes")
                run_as(remote_command("lvdisplay {0}/{1}".format(vg,lv),ip,username))
                print("Integrating hadoop with lvm ")
                directory=input(Fore.YELLOW+"Give the datanode directory"+Style.RESET_ALL)
                run_as(remote_command("mount /dev/{0}/{1} /{2}".format(vg,lv,directory),ip,username))
                run_as(remote_command("hadoop dfsadmin -report",ip,username))
            elif cmd=='23':
                print("extending datanode size")
                vg=input(Fore.YELLOW+"Give the volume group name which is mounted to datanode directory: "+Style.RESET_ALL)
                lv=input(Fore.YELLOW+"Give the logical volume name which is mounted to datanode directory: "+Style.RESET_ALL)
                size=float(input(Fore.YELLOW+"Give how much size to extend the volume in GiB"+Style.RESET_ALL))
                run_as(remote_command("lvextend --size +{0}G /dev/{1}/{2}".format(size,vg,lv),ip,username))
                print("formatting new size")
                run_as(remote_command("resize2fs /dev/{0}/{1}".format(vg,lv),ip,username))
            elif cmd=='24':
                run_as(remote_command("lsblk -o NAME",ip,username))
                print("These are the available volumes and partitions: \n")
                volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                while 1:
                    if check=='y':
                        size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                        print("Checking if you have exceeded the primary partition limit...")
                        primary=int(run_as_(remote_command("lsblk /dev/{} -o TYPE|grep part| wc -l".format(volume),ip,username)))
                        run_as(remote_command('printf n\\\\n\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume),ip,username))
                    elif check=='n':
                        break
                    else:
                        print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                        check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                format_type=input(Fore.YELLOW+"What format type you want to use: "+Style.RESET_ALL)
                print("Formatting the partition...")
                run_as(remote_command("mkfs.{0} /dev/{1}".format(format_type,partition),ip,username))
                run_as(remote_command("udevadm settle",ip,username))
                print("Formated the partition")
                mount=input(Fore.YELLOW+"Give the path to the directory to which you want to mount this partition: "+Style.RESET_ALL)
                run_as(remote_command('mount /dev/{0} {1}'.format(partition, mount),ip,username))
            elif cmd=='25':
                partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                mount=input(Fore.YELLOW+"Give the path to the directory to which you want to mount this partition: "+Style.RESET_ALL)
                run_as(remote_command('mount /dev/{0} {1}'.format(partition, mount),ip,username))
            elif cmd == 'bash':
                run_as(remote_command('',ip,username))
            elif cmd == 'exit':
                break

            else:
                print("Give a proper input you have only the given 21 numbered options, bash and exit")
    elif login=='local':
        if platform.system()=='Linux':
            while 1:
                print(Fore.GREEN+"""
                Select one of the following options:
                1   : run date command
                2   : start webserver
                3   : stop webserver
                4   : start docker process
                5   : stop docker process
                6   : list all the docker containers
                7   : list all the available image
                8   : pull a docker image
                9   : launch a container
                10  : stop a container
                11  : stop all containers
                12  : copy a file to a container
                13  : copy file from the container
                14  : logs of the container
                15  : attach to an existing container
                16  : start hadoop namenode
                17  : start hadoop datanode
                18  : start hadoop client node
                19  : create a primary partition
                20  : create a extended partition
                21  : format a partition
                22  : create lvm and integrate with hadoop
                23  : provide elsticity to datanode
                24  : create static partition and format it and mount it
                25  : mount a partition to a directory
                bash: to start bash shell
                exit: To quit the remote host terminal
                """+Style.RESET_ALL)
                cmd=input(Fore.YELLOW+"Give a command: "+Style.RESET_ALL)
                if cmd == '1':
                    run_as('date')
                elif cmd == '2':
                    run_as('systemctl start httpd;setenforce 0;systemctl stop firewalld')
                    print("Webserver running on http://0.0.0.0:80")
                elif cmd == '3':
                    run_as('systemctl stop httpd;setenforce 1;systemctl start firewalld')
                    print("Webserver stopped which is running on http://0.0.0.0:80")
                elif cmd == '4':
                    run_as('systemctl start docker;setenforce 0;systemctl stop firewalld')
                    print("Docker service is started")
                elif cmd == '5':
                    run_as('systemctl stop docker;setenforce 1;systemctl start firewalld')
                    print("Docker service is stopped")
                elif cmd == '6':
                    run_as('docker ps -a')
                elif cmd == '7':
                    run_as('docker image list')
                elif cmd == '8':
                    image=input(Fore.YELLOW+"Give the image name that u want to download: "+Style.RESET_ALL)
                    run_as('docker pull {}'.format(image))
                elif cmd == '9':
                    name=input(Fore.YELLOW+"Give a name to the container: "+Style.RESET_ALL)
                    opersys=input(Fore.YELLOW+'Give the name of the operating system that u want to launch: '+Style.RESET_ALL)
                    run_as('docker run -dit --name {0} {1}'.format(name,opersys))
                    ask=input(Fore.YELLOW+"Do you want to use the container?(y/n): "+Style.RESET_ALL)
                    while 1:
                        if ask=='y':
                            run_as('docker attach {0}'.format(name))
                            break
                        elif ask=='n':
                            break
                        else:
                            print("Wrong input 'y' and 'n' are consdered as correct inputs")
                            ask=input(Fore.YELLOW+"Do you want to use the container?(y/n): "+Style.RESET_ALL)
                elif cmd=='10':
                    name=input(Fore.YELLOW+"Give a name (or) ID of the container: "+Style.RESET_ALL)
                    run_as('docker stop {0}'.format(name))
                    print("Container {} is stopped".format(name))
                elif cmd=='11':
                    run_as('docker rm -f `docker ps -aq`')
                elif cmd=='12':
                    source_path=input(Fore.YELLOW+"Give the source path"+Style.RESET_ALL)
                    container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                    destination_path=input(Fore.YELLOW+"Give the destination path"+Style.RESET_ALL)
                    run_as("docker cp {0} {1}:{2}".format(source_path,container,destination_path))
                elif cmd=='13':
                    container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                    source_path=input(Fore.YELLOW+"Give the source path"+Style.RESET_ALL)
                    destination_path=input(Fore.YELLOW+"Give the destination path"+Style.RESET_ALL)
                    run_as("docker cp {0}:{1} {2}".format(container,source_path,destination_path))
                elif cmd=='14':
                    container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                    run_as("docker logs {0}".format(container))
                elif cmd=="15":
                    container=input(Fore.YELLOW+"Give container name or ID"+Style.RESET_ALL)
                    run_as("docker attach {0}".format(container))
                elif cmd=='16':
                    print("You need to have the VM launched for configuring the namenode")
                    print("\nCurrent logged in user will be configured as namenode\n")
                    directory=input(Fore.YELLOW+"Give the directory for namenode configuration: "+Style.RESET_ALL)
                    check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                    print("Creating directory...\n")
                    while 1:
                        if check=='y':
                            run_as("rm -rf /{0};mkdir /{0}".format(directory))
                            break
                        elif check=='n':
                            break
                        else:
                            print("Proper input is not given")
                            check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                    if check=='n':
                        continue
                    print("\nConfiguring the namenode's hdfs-site.xml file...\n")
                    save(hdfs_site_name(directory))
                    run_as('cp config_file.txt /etc/hadoop/hdfs-site.xml')
                    print("\nConfiguring the namenode's core-site.xml file...\n")
                    save(core_site_name())
                    run_as('cp config_file.txt /etc/hadoop/core-site.xml')
                    print("Formatting the namenode...\n")
                    run_as('hadoop namenode -format')
                    print("Starting the namenode...")
                    run_as("hadoop-daemon.sh start namenode")
                elif cmd=='17':
                    print("You need to have the VM launched for configuring the datanode")
                    print("\nCurrent logged in user will be configured as datanode\n")
                    namenode=input(Fore.YELLOW+"Give the namenode's IP address: "+Style.RESET_ALL)
                    directory=input(Fore.YELLOW+"Give the directory for datanode configuration: "+Style.RESET_ALL)
                    print("The data in this dir will be deleted if it exists")
                    check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                    while 1:
                        if check=='y':
                            run_as("rm -rf /{0};mkdir /{0}".format(directory))
                            break
                        elif check=='n':
                            break
                        else:
                            print("Proper input is not given")
                            check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                    if check=='n':
                        continue
                    print("\nConfiguring the datanode's hdfs-site.xml file...\n")
                    save(hdfs_site_data(directory))
                    run_as('cp ./config_file.txt /etc/hadoop/hdfs-site.xml')
                    print("\nConfiguring the datanode's core-site.xml file...\n")
                    save(core_site_data(namenode))
                    run_as('cp ./config_file.txt /etc/hadoop/core-site.xml')
                    print("Starting the datanode...")
                    run_as("hadoop-daemon.sh start datanode")
                elif cmd=='18':
                    namenode=input(Fore.YELLOW+"Give the namenode's IP address: "+Style.RESET_ALL)
                    save(core_site_data(namenode))
                    run_as('cp config_file.txt /etc/hadoop/core-site.xml')
                elif cmd=='19':
                    run_as("lsblk -o NAME")
                    print("These are the available volumes and partitions: \n")
                    volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                    check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                    while 1:
                        if check=='y':
                            size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                            print("Checking if you have exceeded the primary partition limit...")
                            primary=int(run_as_("lsblk /dev/{} -o TYPE|grep part| wc -l".format(volume)))
                            if primary<=2:
                                print("You will be able to create a primary partition")
                                run_as('printf n\\\\n\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume))
                            else:
                                print("You will be able to create a primary partition but yo will not be able to create partitions further in this disk after that")
                                print("Hence we don't recommend to create a primary partition u can create a logical partition")
                            break
                        elif check=='n':
                            break
                        else:
                            print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                            check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                elif cmd=='20':
                    run_as("lsblk -o NAME")
                    print("These are the available volumes and partitions: \n")
                    volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                    check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                    while 1:
                        if check=='y':
                            size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                            print("You will be able to create a primary partition")
                            run_as('printf n\\\\ne\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume))
                            break
                        elif check=='n':
                            break
                        else:
                            print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                            check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                elif cmd=='21':
                    run_as("lsblk -o NAME")
                    print("These are the available volumes and partitions: \n")
                    partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                    format_type=input(Fore.YELLOW+"What format type you want to use: "+Style.RESET_ALL)
                    print("Formatting the partition...")
                    run_as("mkfs.{0} /dev/{1}".format(format_type,partition))
                    run_as("udevadm settle")
                    print("Formated the partition")
                elif cmd=='22':
                    run_as("fdisk -l")
                    print("Creating physical volumes")
                    vol1=input(Fore.YELLOW+"Give the name of the first volume"+Style.RESET_ALL)
                    vol2=input(Fore.YELLOW+"Give th name of the second volume"+Style.RESET_ALL)
                    run_as("pvcreate /dev/{}".format(vol1))
                    run_as("pvcreate /dev/{}".format(vol2))
                    print(Fore.YELLOW+"Combining physical volumes")
                    vg=input(Fore.YELLOW+"Give name to volume group: "+Style.RESET_ALL)
                    run_as("vgcreate {0} /dev/{1} /dev/{2}".format(vg,vol1,vol2))
                    print("Information of the volume group")
                    run_as("vgdisplay {vg}".format(vg))
                    print("Creating logical volumes")
                    lv=input(Fore.YELLOW+"Give the logical volume name: "+Style.RESET_ALL)
                    size=float(input(Fore.YELLOW+"Give size in GiB of the logical volume you want to create: "+Style.RESET_ALL))
                    run_as("lvcreate --size {0}G --name {1} {2}".format(size,lv,vg))
                    print("Information about logical volumes")
                    run_as("lvdisplay {0}/{1}".format(vg,lv))
                    print("Integrating hadoop with lvm ")
                    directory=input(Fore.YELLOW+"Give the datanode directory"+Style.RESET_ALL)
                    run_as("mount /dev/{0}/{1} /{2}".format(vg,lv,directory))
                    run_as("hadoop dfsadmin -report")
                elif cmd=='23':
                    print("extending datanode size")
                    vg=input(Fore.YELLOW+"Give the volume group name which is mounted to datanode directory: "+Style.RESET_ALL)
                    lv=input(Fore.YELLOW+"Give the logical volume name which is mounted to datanode directory: "+Style.RESET_ALL)
                    size=float(input(Fore.YELLOW+"Give how much size to extend the volume in GiB"+Style.RESET_ALL))
                    run_as("lvextend --size +{0}G /dev/{1}/{2}".format(size,vg,lv))
                    print("formatting new size")
                    run_as("resize2fs /dev/{0}/{1}".format(vg,lv))
                elif cmd=='24':
                    run_as("lsblk -o NAME")
                    print("These are the available volumes and partitions: \n")
                    volume=input(Fore.YELLOW+"Give the volume in which u want to create partitions: "+Style.RESET_ALL)
                    check=input(Fore.YELLOW+"Are you sure and wanted to continue?(y/n)"+Style.RESET_ALL)
                    while 1:
                        if check=='y':
                            size=float(input(Fore.YELLOW+"Give the size of partition in Giga Bytes"+Style.RESET_ALL))
                            print("Checking if you have exceeded the primary partition limit...")
                            primary=int(run_as_("lsblk /dev/{} -o TYPE|grep part| wc -l".format(volume)))
                            run_as('printf n\\\\n\\\\n\\\\n\\\\n+{0}G\\\\nw|fdisk /dev/{1}'.format(size,volume))
                        elif check=='n':
                            break
                        else:
                            print("Proper input is not given, acceptable inputs are 'y' and 'n' only")
                            check=input(Fore.YELLOW+"Do you want to continue?(y/n): "+Style.RESET_ALL)
                    partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                    format_type=input(Fore.YELLOW+"What format type you want to use: "+Style.RESET_ALL)
                    print("Formatting the partition...")
                    run_as("mkfs.{0} /dev/{1}".format(format_type,partition))
                    run_as("udevadm settle")
                    print("Formated the partition")
                    mount=input(Fore.YELLOW+"Give the path to the directory to which you want to mount this partition: "+Style.RESET_ALL)
                    run_as('mount /dev/{0} {1}'.format(partition, mount))
                elif cmd=='25':
                    partition=input(Fore.YELLOW+"Give the partition name which you want to format: "+Style.RESET_ALL)
                    mount=input(Fore.YELLOW+"Give the path to the directory to which you want to mount this partition: "+Style.RESET_ALL)
                    run_as('mount /dev/{0} {1}'.format(partition, mount))
                elif cmd == 'bash':
                    run_as('bash')
                elif cmd == 'exit':
                    break
                else:
                    print("Give a proper input you have only the given 21 numbered options, bash and exit")
        elif platform.system()=="Windows":
            print("""
            We dont have commands for windows operating system we can only give a cmd for you
            """)
            run_as("cmd")
    elif login=='aws':
        while True:
            print("\n\n\t\t\t\t\t\t\t||||||||||||||||||||||||")
            print("\t\t\t\t\t\t\t...WELCOME TO MY MENU...")
            print("\t\t\t\t\t\t\t||||||||||||||||||||||||")
            print("""\n
            press 1  :CREATE KEY PAIR
            press 2  :CREATE SECURITY GROUP
            press 3  :LAUNCE NEW AWS INSTANCE
            press 4  :START INSTANCE
            press 5  :TERMINATE INSTANCE
            press 6  :STOP INSTANCE
            press 7  :CREATE EBS VOLUME
            press 8  :ATTACH EBS VOLUME TO INSTANCE
            press 9  :DETACH EBS VOLUME
            press 10 :DELETE EBS VOLUME
            press 11 :CREATING S3 BUCKET
            press 12 :UPLOAD DATA IN  S3 BUCKET
            press 13 :CREATING CLOUDFRONT DISTRIBUTION
            press 14 :CREATE SNAPSHOT 
            PRESS 15 :QUIT
            """)
            ch = input("\t\t\t\t\t\tENTER YOUR CHOICE :")
            if ch =='1':
                    pyttsx3.speak("......START TO CREATE PAIR KEY FOR YOU..... ")
                    print("......START TO CREATE PAIR KEY FOR YOU..... ")
                    run_as("aws ec2 create-key-pair --key-name mykey --query 'KeyMaterial' --output text > mykey.pem")
                    pyttsx3.speak(" ....PAIR KEY CREATED SUCCESSFULLY..... ")
                    print(" ....PAIR KEY CREATED SUCCESSFULLY..... ")
            elif ch =='2':
                    pyttsx3.speak("...CREATING SECURITY GROUP FOR YOU...")
                    print("...CREATING SECURITY GROUP FOR YOU...")
                    run_as("aws ec2 create-security-group --group-name mysecuritygroup --description my-sg ")
                    pyttsx3.speak(" ....SECURITY GROUP CREATED SUCCESSFULLY..... ")
                    print(" ....SECURITY GROUP CREATED SUCCESSFULLY....")
            elif ch =='3':
                    pyttsx3.speak("..PROVISIONING NEW AWS INSTANCE FOR YOU...")
                    x=input("ENTER SECURITY GROUP ID :")
                    y=input("ENTER KEY PAIR NAME :")
                    run_as("aws ec2 run-instances --image-id ami-052c08d70def0ac62 --instance-type t2.micro --count 1 --subnet-id subnet-712d2419 --security-group-ids {0} --key-name {1}".format(x,y))
                    pyttsx3.speak(" ....AWS INSTANCE LAUNCHED SUCCESSFULLY..... ")
            elif ch =='4':
                    x=input("ENTER INSTANCE ID :")
                    pyttsx3.speak(".starting INSTANCE FOR YOU...")
                    run_as("aws ec2 start-instances --instance-ids {}".format(x))
                    pyttsx3.speak(" ....AWS INSTANCE start SUCCESSFULLY..... ")
            elif ch =='5':
                    x=input("ENTER INSTANCE ID :")
                    pyttsx3.speak("TERMINATING INSTANCE FOR YOU...")
                    run_as("aws ec2 terminate-instances --instance-ids {}".format(x))
                    pyttsx3.speak(" ....AWS INSTANCE terminate SUCCESSFULLY..... ")
            elif ch =='6':
                    x=input("ENTER INSTANCE ID :")
                    pyttsx3.speak("STOPPING INSTANCE FOR YOU...")
                    run_as("aws ec2 stop-instances --instance-ids {}".format(x))
                    pyttsx3.speak(" ....AWS INSTANCE stop SUCCESSFULLY..... ")
            elif ch =='7':
                    pyttsx3.speak("..CREATING EBS VOLUME FOR YOU...")
                    run_as("aws ec2 create-volume  --volume-type gp2 --size 1  --availability-zone ap-south-1a")
                    pyttsx3.speak(" ....EBS VOLUME  CREATED SUCCESSFULLY..... ")
            elif ch =='8':
                    x=input("ENTER VOLUME ID :")
                    y=input("ENTER INSTANCE ID :")
                    pyttsx3.speak("..ATTACHING EBS VOLUME FOR YOU...")
                    run_as("aws ec2 attach-volume  --volume-id {0} --instance-id {1} --device /dev/sdf".format(x,y))
                    pyttsx3.speak(" ....EBS VOLUME  ATTACHED SUCCESSFULLY..... ")
            elif ch =='9':
                    x=input("ENTER VOLUME ID :")
                    pyttsx3.speak("..DETACHING EBS VOLUME FOR YOU...")
                    run_as("aws ec2 detach-volume  --volume-id {} ".format(x))
                    pyttsx3.speak(" ....EBS VOLUME  ATTACHED SUCCESSFULLY..... ")
                    print(" ....EBS VOLUME  ATTACHED SUCCESSFULLY..... ")
            elif ch =='10':
                    x=input("ENTER VOLUME ID :")
                    pyttsx3.speak("..DELETING EBS VOLUME FOR YOU...")
                    run_as("aws ec2 delete-volume  --volume-id {}".format(x))
                    pyttsx3.speak(" ....EBS VOLUME  DELETED SUCCESSFULLY..... ")
            elif ch =='11':
                    pyttsx3.speak(". creating bucket ..")
                    x=input("ENTER BUCKET NAME :")
                    run_as("aws s3 mb s3://{}".format(x))
                    pyttsx3.speak(".s3 bucket created successfully..")
                    print(".s3 bucket created successfully..")
            elif  ch =='12':
                    pyttsx3.speak("..uploading data in s3 bucket.")
                    x=input("ENTER STATIC DATA NAME :")
                    y=input("ENTER s3 bucket name NAME :")
                    run_as("aws s3 cp {0} s3://{1}".format(x,y))  
                    pyttsx3.speak(".in s3 bucket image is uploaded successfully..")
            elif  ch =='13':
                    pyttsx3.speak("..WE ARE CREATING CLOUNDFRONT DISTRIBUTION.")
                    x=input("ENTER S3 BUCKETNAME NAME :")
                    y=input("ENTER STATIC DATA NAME :")
                    run_as("aws cloudfront create-distribution --origin-domain-name {0}.s3.amazonaws.com --default-root-object {1}".format(x,y))  
                    pyttsx3.speak(".we successfully created cloud front distribution..")
            elif  ch =='14':
                    pyttsx3.speak("..WE ARE CREATING snapshot.")
                    x=input("ENTER VOLUME ID :")
                    run_as("aws ec2 create-snapshot --volume-id {}".format(x))
            elif  ch =='15':
                    pyttsx3.speak("you choose... to go outside the menu... bye... take care...")
                    break
            else:
                    print("YOU ENTERED WRONG CHOICE HERE !! ..PLEASE SELECT CHOICE FROM MENU...! ")
                    pyttsx3.speak("YOU ENTERED WRONG CHOICE HERE !! ..PLEASE SELECT CHOICE FROM MENU...! ")
    else:
        print("You have selected option which is not available choose from 'local','remote','aws'")
