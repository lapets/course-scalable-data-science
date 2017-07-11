To run a sample job on your cluster, please follow the steps below:

Part 1:

We will be using Github gists for writing code. If you want to know more about how gists work, please go through the following tutorial: https://help.github.com/articles/about-gists/

1. The first thing you should know is how to setup a github gist workflow.

    * Go to https://gist.github.com/ and create a new gist with title job.py

    * Copy the gist url at the top of the webpage

Part 2:
2. Now you need to SSH into the master machine for your cluster. For linux and mac, the SSH utility comes by default. For windows, try installing a client like PuTTY: http://www.putty.org/ and use a command line interface.

   Login into your cluster's master node using SSH :

       `ssh -i britetest.pem <root@ip>`
  
   where ip is the public ip of your cluster's master node.
  
3. Once logged into the machine, you are in the root directory of the instance. Here, git clone your github gist. Do that by copying the url at the top of your webpage for the gist, and running:

    `git clone <url>`

4. Your Master's home folder has a spark folder with a bin folder inside it. If the job is in /mygist/job.py, now you can run the job in a distributed fashion as:
   
   ```./spark/bin/spark-submit /mygist/job.py```


If you want to update the code, based on whether or not you have a github account, please follow the steps below:
    
  * If you are logged into github, you can simply edit your code online in the github gist interface and in the master machine:
  
       * cd into the gist folder using ```cd mygist/```    
       * Pull the new code using ```git pull```
        
  * If you are not logged in, please create a new gist everytime you change your code, clone the new gist into your master machine's home directory run the job file as shown above. (Step 3)

Now run the job as was done in step 4
