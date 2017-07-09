#!/bin/bash

mkdir -p aws_log
for i in {1..5}
do
   echo "Welcome $i times"
   
   #./spark-setup/ec2/spark-ec2 -k britetest -i britetest.pem -s 2  --instance-type="t2.micro" launch group_n_cluster >> aws_log/group_n_cluster.log  
   ./spark-setup/ec2/spark-ec2 -k britetest -i britetest.pem -s 2  --instance-type="t2.micro" launch group$i-cluster >> aws_log/group$i-cluster.log
done
