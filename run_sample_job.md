To run a sample job on your cluster, please follow the steps below:

* You need to SSH into the machine. For linux and mac, it comes by default. For windows, try installing a client like PuTTY: http://www.putty.org/

* Login into your cluster's master node using SSH :

    `ssh -i britetest.pem <root@ip>`
  
  where ip is the public ip of your cluster's master node.
  
* Once logged into the machine, you are in the root directory of the instance. Here, git clone your github gist. Do that by copying the url at the top of your webpage for the gist, and running:

    `git clone <url>`

* Your Master's home folder has a spark folder with a bin folder inside it. If the job is in /mygist/job.py, now you can run the job in a distributed fashion as:
   
   ```./spark/bin/spark-submit /mygist/job.py```
