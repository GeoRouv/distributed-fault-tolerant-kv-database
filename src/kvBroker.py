import sys
import getopt
import json
import socket
import errno
import random
import time


def checkServerStatus(serversInfo, k):
    '''
    Returns 1 if k servers are down
    Returns 2 if at least one server is down
    Prints warning message if at least two servers are down

    @k: replication factor 
    @serversinfo: list containing the servers info 
    '''

    counter = 0
    for server in serversInfo:
        ip_address = server[0]
        PORT = int(server[1])
        s = socket.socket()

        try:
            s.connect((ip_address, PORT))
        except:
            counter += 1
        s.close()

    if counter >= 2:
        print(
            "\n> WARNING: Two or more servers are down. Correct output not guaranteed.\n")

    if counter == k:
        print("\n> kvBroker can't operate with k servers down.")
        return 1

    if counter >= 1:
        return 2

    return 0


def getRandServerIndices(k, serversInfo):
    '''
    Returns a list of random indices of servers from serversinfo

    @k: replication factor - number of indices returned
    @serversinfo: list containing the servers info 
    '''

    indexes = []
    for _ in range(k):
        r = random.randint(0, len(serversInfo)-1)
        while(r in indexes):
            r = random.randint(0, len(serversInfo)-1)
        indexes.append(r)

    return indexes


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "hk:s:i:k:")
    except getopt.GetoptError:
        print("\nInvalid arguments. See usage below:\n\n")
        print('python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k <int>\n')
        sys.exit(2)

    if len(opts) < 3:
        print("\nSome arguments are missing. See usage below:\n\n")
        print('python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k <int>\n')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                'python3 kvBroker.py -s serverFile.txt -i dataToIndex.txt -k <int>\n')
            sys.exit()
        elif opt in ("-s"):
            serverfile = arg
        elif opt in ("-i"):
            dataToIndex = arg
        elif opt in ("-k"):
            k = int(arg)

    # Reading output data from the previous part
    with open(dataToIndex) as f:
        data = [line.rstrip(" \\\n").replace(" ", "") for line in f]

    # Parse servers info
    serversInfo = []
    with open(serverfile) as f:
        for line in f:
            serversInfo.append(line.split())
    if(len(serversInfo) < k):
        print("Not as many servers as the k number!\nPlease reduce -k or change -s file.")
        sys.exit()

    # ============= Server Indexing  ==========
    print("\nStarting indexing of servers...\n")

    # Connect to servers and send all data
    for i in data:
        # fetch a list of random k servers to send data
        serverIndices = getRandServerIndices(k, serversInfo)
        for index in serverIndices:

            ip_address = serversInfo[index][0]
            PORT = int(serversInfo[index][1])
            s = socket.socket()
            try:
                s.connect((ip_address, PORT))

                dataToSend = "PUT " + i
                s.send(dataToSend.encode())

                dataFromServer = s.recv(4098)
                print(
                    f"Response from {ip_address}:{PORT}: {dataFromServer.decode()}")
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    print(f"Connection refused for {ip_address}:{PORT}")
                else:
                    print("Caught exception socket.error : %s" % e)
            s.close()
        print("====================================")
    print("\nIndexing finished!\n")

    # Check if servers are down
    if checkServerStatus(serversInfo, k) == 1:
        print("\nExitting...")
        return

    # =========== Serving Queries ==============
    print("-Type a query:\n")
    for line in sys.stdin:
        if ("" == line.rstrip()):
            continue
        # exit keyword
        if ('EXIT' == line.rstrip()):
            break

        # Check if servers are down
        if (checkServerStatus(serversInfo, k)) == 1:
            break

        # Disable further PUT requests after indexing
        temp = line.split()
        if temp[0] == "PUT":
            print("\n> PUT requests are not supported after server indexing.")
            continue

        if temp[0] == "DELETE":
            if (checkServerStatus(serversInfo, k)) == 2:
                print("\n========== Query Results ===========")
                print(
                    "> DELETE request cannot be reliably executed because at least one server is down.")
                print("====================================\n")
                print("\n-Type a query:\n")
                continue

        print("\n========== Query Results ===========")

        # Send request to all servers linearly
        for server in serversInfo:
            ip_address = server[0]
            PORT = int(server[1])
            s = socket.socket()

            try:
                s.connect((ip_address, PORT))
                dataToSend = line
                s.send(dataToSend.encode())

                dataFromServer = s.recv(4098)
                print(
                    f"> Response from {ip_address}:{PORT}:\n-> {dataFromServer.decode()}")

                if ":" in dataFromServer.decode():
                    break
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    print(f"> Connection refused for {ip_address}:{PORT}")
                else:
                    print("> Caught exception socket.error : %s" % e)
            s.close()
        print("====================================\n")
        print("\n-Type a query:\n")

    print("\nExitting...\n")


if __name__ == "__main__":
    main(sys.argv[1:])
