import requests
import json

# read test cases from filesystem
# Reading from tests.json
def fetch_test_cases():
    with open("tests.json", "r") as cases:
        return json.load(cases)

# define app info
host = "http://localhost"
port = "5050"

# retrieve all test cases from file system
cases = fetch_test_cases()

# iterate through all tests
for number, testCase in enumerate(cases):

    # display extract test information
    characterName = testCase['name']
    characterExpectedConfig = testCase['expectedConfig']
    caseUri = "/view/{}/data".format(characterName)
    passed = 0

    # concatenate all variables & create URL
    url = host + ":" + port + caseUri

    # fetch records from API
    characterActualConfig = requests.get(url, verify=False).json()
    
    # display test information
    print("\n#####################################################")
    print("Test Case #: {}".format(number))
    print("Character Name: {}".format(characterName))
    print("Expected Characters Total: {}".format(len(characterExpectedConfig)))
    print("Actual Characters Total: {}".format(len(characterActualConfig)))

    # traverse through all records
    for index, (actual, expected) in enumerate(zip(characterActualConfig, characterExpectedConfig)):

        # determine if records match
        matching = actual == expected

        # check for equality between dictionary records
        if not matching:
            print("")
            print("CASE INDEX: {}, DISCREPANCY FOUND".format(index))
            print("")
            #print("Actual: {}".format(json.dumps(actual, indent=4)))
            #print("Expected: {}".format(json.dumps(expected, indent=4)))
        else:
            #print("CASE INDEX: {}, NO ISSUES".format(index))
            passed += 1

    print("PASSED CASES: {}/{}".format(passed,len(characterActualConfig)))