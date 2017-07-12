#!/bin/bash
#Just this will not do, you need to have appropriate keys to run this file!
echo "You are about to execute the $1 command for the $2 cluster"

for i in {1..5}
do
   echo "You are about to execute the $1 command for the group$i-cluster"
   ./spark-setup/ec2/spark-ec2 -k britetest -i britetest.pem $1 group$i-cluster
done
