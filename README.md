# distributed-fault-tolerant-kv-database
A simple version of a distributed, fault-tolerant, Key-Value (KV) database (or store), with a few tweaks. 


## Prerequisites
---
• Make sure you have python3 (preferably 3.8.5) installed.
• All libraries used are part of the python standard library.
• This implementation contains the last task for using only the trie data structure for
indexing and searching all of the keys (both top-level and within the values and the
nesting) and no other data structure.
• The folder under the name ”src” contains all the source code and the input-output
data files, so terminals - commands must be run inside that directory.
• Read more details on the implementation plan in "Project Report" pdf file.


## Instructions
---

### Data Creation

Run the following command to create data for the next steps:

    $python3 createData.py -k keyFile.txt -n 15 -d 2 -l 15 -m 8

where,
-n: indicates the number of lines (i.e. separate data) that we would like to generate 
-d: maximum level of nesting
-m: maximum number of keys inside each value
-l: maximum length of a string value when generated
-k keyFile.txt: file containing a space-separated list of key names and their data types (this is already included, supports {int, float, string})

### Key Value Store
1.kvServer

First of all, launch the servers (at localhost) using the following command(s):

    $python3 kvServer.py -a 127.0.0.1 -p 8000
    $python3 kvServer.py -a 127.0.0.1 -p 8001
    $python3 kvServer.py -a 127.0.0.1 -p 8002
    $python3 kvServer.py -a 127.0.0.1 -p 8003

where,
-a is the (localhost) ip_address
-p is the port


2.kvBroker

After servers are on, use the command below to launch the client:

    $python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k 4

where,
-s is a text file indicating that this broker will be working with a numbers servers with the IPs described and on the respective ports described
-i is a file containing data that was output from the previous part of the projectthat was generating the data
-k is the replication factor, i.e. how many different servers will have the same replicated data.

Indexing should then start, and after is finished, KVbroker accepts queries from standard input. Some examples (using the data file in the src directory):

    $GET person0
    $GET person9
    $QUERY person9.level.age
    $QUERY person8.hair_color
    $DELETE person3
    $GET person3
    $QUERY person3.age
    $EXIT

To exit the CLI mode of kvBroker type "EXIT". 



The commands listed in this README were mainly used for debugging/testing.
Feel free to change the parameters as you desire.
