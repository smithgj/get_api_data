import sys
import requests


def parseOptions():
    # do this and help
    #print(sys.argv[0])
    #print(sys.argv[1:])
    if len(sys.argv) == 1 or '-h' in sys.argv:
        printHelp()
        sys.exit(0)
    if '-u' not in sys.argv:
        print("no url (-u) provided, exiting")
        sys.exit(0)
    if '-u' in sys.argv and '-g' in sys.argv and len(sys.argv) == 4:
        return ('g')
    if '-u' in sys.argv and '-g' in sys.argv and '-v' in sys.argv and len(sys.argv) == 5:
        return ('gv')
    if ('-u' and '-n' and '-k' in sys.argv):
        if ("-c" and "-w" in sys.argv and len(sys.argv) ==11):
            return('cw')
        elif ("-c" and "-w" and '-v' in sys.argv and len(sys.argv) ==12):
            return('cwv')
        elif ("-s" in sys.argv and len(sys.argv) ==9):
            return('s')
        elif ("-s" and '-v' in sys.argv and len(sys.argv) ==10):
            return('sv')
        else:
            print("Incompatible/missing command line arguments, exiting")
            sys.exit()



def printHelp():
    print("\n")
    print("check_namespaced_xml.py or check_namespaced_xml.py -h prints this help")

    print("This plugin reads an xml from a webserver (api) and allows you to compare a value you enter")
    print("to a key in the xml.")
    print("\n")
    print("Command line arguments:")
    print("-u <url>  required - ex http://airtraffic.com/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=fltData")
    print("-g will list all namespaces, attributes, and keys in the XML, must be used with -u only")
    print("-n <namespace>  this is the namespace for the key of interesust be used with the -k optiont, m")
    print("-k <key>  this is the key of the data in the xml, must be used with the -n option")
    print("Submit the values for comparison as shown:")
    print("   for a numeric key use -w for the warning value and -c for the critical value if you")
    print("     want to trigger alerts based on the value of the key.")
    print("   for a string key use -s")
    print("     the -s may also be used if you want an exact match for a numeric key")
    print("     note -for dates and timestamps use the -s (this may be improved upon in the future)")
    print("\n")
    print("-v can be used to print a lot of debug data")

def loadData(debug):
    # get xml data as one long string
    req = requests.request('GET', "https://wtc.vaisala.com/nm10/geoserver/vaisala/ows?service=WFS&version=1.1.0&request=GetFeature&typeName=vaisala:latestObservations&sortby=vaisala:source&filter=%3CFilter%3E%3CAnd%3E%3CPropertyIsEqualTo%3E%3CPropertyName%3Evaisala:source%3C/PropertyName%3E%3CLiteral%3EWTC%3C/Literal%3E%3C/PropertyIsEqualTo%3E%3CPropertyIsEqualTo%3E%3CPropertyName%3Evaisala:capability_name%3C/PropertyName%3E%3CLiteral%3EVAISALA_SURFACE_OBS/AQTS_NO_UNIT_VALUE_PT1M_1%3C/Literal%3E%3C/PropertyIsEqualTo%3E%3C/And%3E%3C/Filter%3E")
    a = str(req.text)
    if (debug): print(a)

    chunks = a.split('<')
    if (debug): print (chunks)
    return chunks

def getNamespaces(debug, chunks, dataElements):
    namespaces = []
    if (debug): print("The elements are:")
    for element in chunks:
        element = '<' + element
        if len(element) > 1:
            if element[1] != '?' and element[1] != '/':
                dataElements.append(element)
                if (debug): print(element)
                #namespace is in between < and : let's get them
                namespace = element[1:element.find(':')]
                if namespace not in namespaces:
                    namespaces.append(namespace)
    if (debug):
        print('\n' + 'namespaces = ')
        print(namespaces)
    return(namespaces)

def organizeData(debug, namespaces, dataElements):
    #group attributes, nodes, keys by namespace
    namespaceDataDict={}

    for i in namespaces:
        # for the i^th namespace get all its elements and assign to dataList
        dataDict = {}
        for j in dataElements:
            if j[1:j.find(':')] == i:
                if (debug): print('adding ' + j + ' to ' + i)
                if j[-1] == '>':  # i am an attribute or node
                    if ' ' in j:  #attribute
                        key = 'attribute = ' + j[j.find(':')+1:j.find(' ')]
                        value = j[j.find(' '):-1]
                        dataDict[key] = value
                    else:
                        key = 'node'
                        value = j[j.find(':')+1:-1]
                        dataDict[key] = value
                else:    # j will look like:   <namespace:key>value - note no closing >
                    key = j[j.find(':')+1:j.find('>')]
                    value = j[j.find('>')+1:]
                    dataDict[key] = value


        namespaceDataDict[i] = dataDict
    if (debug):
        print("namespaceDataDict =")
        print (namespaceDataDict)
    return namespaceDataDict

def returnAll(debug, namespaces, orgData):
    if (debug):
        print("namespaces = ")
        for n in namespaces:
            print(n)
    for eachkey in orgData.keys():
        print('namespace = ' + eachkey)
        tempDict = orgData.get(eachkey)
        for key in tempDict:
            print('     ' + key + ': ' + tempDict.get(key) )
def main():
    debug = False
    mode = ''
    namespaces = []
    dataElements = []
    orgData = {}

    mode = parseOptions()
    if 'v' in mode:
        debug = True

    if (debug): print("mode set to: " + mode)

    chunks = loadData(debug)
    namespaces = getNamespaces(debug, chunks, dataElements)
    orgData = organizeData(debug, namespaces, dataElements)

    # if -g option was used then spit out all info and quit
    if 'g' in mode:
        returnAll(debug, namespaces, orgData)

    # compare data to value
    if 'cw' in mode:
        print('cw')

    if 's' in mode:
        print('s')

if __name__ == "__main__":
    # calling main function
    main()