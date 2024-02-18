
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
          'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

"""
Returns true if a file ends in .json
"""


def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'


"""
Converts month to a number, e.g. 'Dec' to '12'
"""


def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon


"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""


def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]


"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""


def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


"""
return "NULL" if a string is None, else return itself
"""
def checkNone(str):
    return str if str is not None else "NULL"

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""


def parseJson(json_file):
    fields = ["Name","Category","Currently","Buy_Price","First_Bid","Number_of_Bids","Bids","Location","Country","Started","Ends","Seller","Description"]

    with open(json_file, 'r') as f:
        # creates a Python dictionary of Items for the supplied json file
        json_file = loads(f.read())['Items']

        items = open("items.dat", "a")
        categories = open("categories.dat", "a")
        bids = open("bids.dat", "a")
        bidders = open("bidders.dat", "a")
        sellers = open("seller.dat", "a")
        for item in json_file:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            itemID = item["ItemID"]
            items.write(itemID)
            for field in fields:
                try:
                    match field:
                        case "Category":
                            if (item[field] is not None):
                                cats = item[field]
                                for cat in cats:
                                    cat = cat.replace('"','""')
                                    categories.write(f"{itemID}|\"{cat}\"\n")

                        case "Currently"|"Buy_Pricce"|"First_Bid":
                            items.write("|")
                            items.write(transformDollar((item[field])))

                        case "Bids":
                            if (item[field] is not None):
                                bs = item[field]
                                for bid_obj in bs:
                                    bid = bid_obj["Bid"]
                                    bdr = bid["Bidder"]
                                    bdrID = bdr["UserID"].replace('"','""')
                                    bids.write("{}|\"{}\"|\"{}\"|{}\n".format(itemID, bdrID, transformDttm(bid["Time"]),transformDollar(bid["Amount"])))
                                    bidders.write("\"{}\"|{}".format(bdrID.replace('"','""'), bdr["Rating"]))
                                    try:
                                        bidders.write("|\"{}\"".format(bdr["Location"].replace('"','""')))
                                    except KeyError:
                                        bidders.write("|")
                                    try:
                                        bidders.write("|\"{}\"\n".format(bdr["Country"].replace('"','""')))
                                    except KeyError:
                                        bidders.write("|\n")

                        case "Started"|"Ends":
                            items.write("|")
                            items.write(transformDttm(item[field]))

                        case "Seller":
                            slr = item[field]
                            sellers.write("{}|\"{}\"|{}\n".format(itemID, slr["UserID"].replace('"','""'), slr["Rating"]))

                        case _:
                            items.write("|")
                            items.write("\"{}\"".format(checkNone(item[field]).replace('"','""')))
                            
                except KeyError:
                    continue
            items.write("\n")

        items.close()
        categories.close()
        bids.close()
        bidders.close()
        sellers.close()
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""


def main(argv):
    if len(argv) < 2:
        print('Usage: python skeleton_json_parser.py <path to json files>',
              file=sys.stderr)
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print("Success parsing ", f)


if __name__ == '__main__':
    main(sys.argv)
