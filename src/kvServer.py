import sys
import getopt
import socket
import trie
import json

# Helper Function
def dictModifier(myDict, prefix=None, result={}):
    '''
    'Unpacks' and returns a dictionary using all the nested key-values

    @myDict: dictionary to be modified
    @prefix: prefix string to maintain
    @result: final dictionary
    '''

    for key in myDict:
        if prefix is None:
            prefix_str = (str(key))
        else:
            prefix_str = (prefix, str(key))
            prefix_str = '.'.join(prefix_str)

        if isinstance(myDict[key],dict):
            dictModifier(myDict[key], prefix_str, result)

        if prefix_str not in result:
            result[prefix_str] = myDict[key]

    return result


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "hk:a:p:")
    except getopt.GetoptError:
        print("\nInvalid arguments. See usage below:\n\n")
        print('kvBroker -s serverFile.txt -i dataToIndex.txt -k <int>\n')
        sys.exit(2)

    if len(opts) < 2:
        print("\nSome arguments are missing. See usage below:\n\n")
        print('python3 kvServer.py -a <ip_address> -p <port>\n')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                'python3 kvServer.py -a <ip_address> -p <port>\n')
            sys.exit()
        elif opt in ("-a"):
            ip_address = arg
        elif opt in ("-p"):
            PORT = int(arg)

    database = trie.Trie()

    # create a socket object
    s = socket.socket()
    print("Socket successfully created!")
    # bind to port
    s.bind((ip_address, PORT))
    print("Socket binded to %s." % (PORT))

    # socket in listening mode (up to 5 connections)
    s.listen(5)
    print("Socket is listening...")
    while True:
        # Establish connection with client.
        c, addr = s.accept()
        print('Got connection from: ', addr)

        dataFromClient = c.recv(4098)

        # if client data was empty ignore query handling
        if(len(dataFromClient) <= 0):
            continue

        dataFromClient = dataFromClient.decode().split()

        # ========= PUT Request ==========
        if dataFromClient[0] == "PUT":
            print(
                f"Received PUT request. Adding to database:\n{dataFromClient[1]}\n")

            temp = "{" + dataFromClient[1] + "}"
            temp = temp.replace("'", "\"")
            temp = json.loads(temp)


            # If high-level keys exist already, don't overwrite
            if not database.search(str(list(temp.keys())[0]))[0]:
                myDict = dictModifier(temp)

                for key in myDict:
                    database.insert(key, myDict[key])
                response = "OK"
            else:
                response = "High-level key already exist. Overwrite is not supported."

        # ========= GET Request ==========
        elif dataFromClient[0] == "GET":
            if "." in dataFromClient[1]:
                response = "ERROR - No high-level key specified"
            else:
                result = database.search(dataFromClient[1])
                if result[0]:  # if key found
                    response = dataFromClient[1] + ": " + str(result[1])
                else:
                    response = "NOT FOUND - " + \
                        str(dataFromClient[1]) + " is not a high-level key"

        # ========= QUERY Request ==========
        elif dataFromClient[0] == "QUERY":
            result = database.search(dataFromClient[1])

            if result[0]:  
                response = dataFromClient[1] + ": " + str(result[1])
            else:
                response = "NOT FOUND - " + \
                    str(dataFromClient[1]) + " is not a key"

        # ========= DELETE Request ==========
        elif dataFromClient[0] == "DELETE":
            result = database.delete(dataFromClient[1])

            if "." in dataFromClient[1]:
                response = "ERROR - No high-level key specified"
            else:
                if result:  
                    response = dataFromClient[1] + " has been deleted"
                else:
                    response = "NOT FOUND - " + \
                        str(dataFromClient[1]) + " is not a key"

        # ========= ELSE ==================
        else:
            response = "ERROR - No request of this type available"

        c.send(response.encode())


if __name__ == "__main__":
    main(sys.argv[1:])
