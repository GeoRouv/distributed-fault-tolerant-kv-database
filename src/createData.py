import sys
import getopt
import random

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

def CreateRandStr(alphabet, max_str_len):
    '''
    Returns a random string

    @alphabet: characters to use
    @max_str_len: max string length
    '''

    rand_str = ""  # create an empty string
    chr_cnt = 0  # how many characters of the string we have determined so far
    while chr_cnt < random.randint(1, max_str_len):
        rand_str = rand_str + alphabet[random.randint(0, len(alphabet)-1)]
        chr_cnt = chr_cnt + 1
    return rand_str


def payloadGenerator(keyTypes, nesting, max_keys, max_str_length):
    '''
    Returns payload for each high-level key

    @keyTypes: list of keys and their types
    @nesting: maximum level of nesting
    @max_keys: maximum number of keys inside a value
    @max_str_length:
    '''
    payloadDict = {}

    usedIndexes = []
    # Add up to $max_keys keys to payload
    for _ in range(0, random.randint(0, max_keys)):

        # 33% chance of creating a nesting
        produceProb = random.choice([0, 2])
        # produce random index to select a keytype from its list
        index = random.randint(0, max_keys-1)
        # check if a key exists already in the same level and if not change it to an available
        if index not in usedIndexes:
            usedIndexes.append(index)
        elif (len(usedIndexes) != max_keys):
            while index in usedIndexes:
                index = random.randint(0, max_keys-1)
        else:
            continue

        # if $produceProb has value of 1, then a nesting is create calling recursively the same function
        if(nesting > 0 and produceProb):
            payloadDict[keyTypes[index][0]] = payloadGenerator(
                keyTypes, nesting - 1, max_keys, max_str_length)
        # else fill in with a random key value
        else:
            if(keyTypes[index][1] == "string"):
                value = CreateRandStr(ALPHABET, max_str_length)
            if(keyTypes[index][1] == "int"):
                value = str(random.randint(1, 100))
            if(keyTypes[index][1] == "float"):
                value = str(round(random.uniform(1.5, 2.1), 2))
            payloadDict[keyTypes[index][0]] = value

    return payloadDict


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "hk:n:d:l:m:")
    except getopt.GetoptError:
        print("\nInvalid arguments. See usage below:\n\n")
        print('createData.py -k keyFile.txt -n <int> -d <int> -l <int> -m <int>\n')
        sys.exit(2)

    if len(opts) < 5:
        print("\nSome arguments are missing. See usage below:\n\n")
        print('createData.py -k keyFile.txt -n <int> -d <int> -l <int> -m <int>\n')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(
                'createData.py - k keyFile.txt - n < int > -d < int > -l < int > -m < int >\n')
            sys.exit()
        elif opt in ("-k"):
            inputfile = arg
        elif opt in ("-n"):
            lines = int(arg)
        elif opt in ("-d"):
            nesting = int(arg)
        elif opt in ("-l"):
            max_str_length = int(arg)
        elif opt in ("-m"):
            max_keys = int(arg)

    # parsing key names-types
    myfile = open(inputfile, 'r')
    keyTypes = []
    for i in myfile.readlines():
        keyTypes.append(i.split())

    # data generation
    myDict = {}
    for j in range(lines):
        myDict['\'person' + str(j)+'\''] = payloadGenerator(keyTypes,
                                                     nesting, max_keys, max_str_length)

    # write generated data to file
    with open("dataToIndex.txt", 'w') as f:
        for d in myDict:
            f.write(d + ":" + str(myDict[d]))
            f.write('\n')


if __name__ == "__main__":
    main(sys.argv[1:])
