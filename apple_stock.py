from bs4 import BeautifulSoup
import urllib2

__author__ = 'Patrick Abejar'


'''This function will find the column number of a given header title with the
left most column being represented as 0 incremeted by 1 in the rightward dir-
ection. It does this by searching for the given header title for all the
string contents of the <th></th> tags in the soup. Once it has found the app-
licable <th></th> tags, it will determine what order the <th></th> tag is in
the row by taking a look at its parent and iterating through all the children
to determine what order from the left most column contains the header. This
also returns the row which contains the header found.
'''


def find_column(input_soup, header):

    # Since a labeled column is being searched for, <th> is appropriate since
    # it contains this information.
    table = input_soup.find_all('th')
    date_column = None
    header_row = None

    # Searches through all the table header <th> tags' string entries to find
    # where the input header is found in the BeautifulSoup object.
    for entry in table:
        if entry.string.lower() == header.lower():

            # When the input header is found, a parent view is obtained in
            # order to search for the <td> cell's position from the first
            # <td> cell (or a.k.a. first parent's child)
            for i in range(0, len(entry.parent.contents)):
                if entry.parent.contents[i] == entry:
                    date_column = i
                    header_row = entry.parent

    # First list item returned is the column position of the header
    # Second list item returned is access to the row of the header
    return date_column, header_row


'''This script takes a response from the Yahoo! Finance website and parses
through data in order to find the historic stock data for AAPL. This will be
displayed to users' screen.
'''


def main():

    print "The following information about AAPL's stock was retrieved from" \
          " finance.yahoo.com.\n(URL: http://finance.yahoo.com/q/hp?s=AAPL" \
          "+Historical+Prices)\n"

    # Take a request from finance.yahoo.com in order to receive the historical
    # stock data in a response. (It is interesting to note that changing the
    # stock ticker from AAPL to any valid ticker in the URL changes the data
    # printed to the corresponding company flawlessly.)
    req = urllib2.Request("http://finance.yahoo.com/q/hp?s=AAPL+Historical"
                          "+Prices")
    res = urllib2.urlopen(req)
    html_doc = res.read()
    soup = BeautifulSoup(html_doc, 'html5lib')

    # The column locations are stored from the find_column() method
    date_col_loc = find_column(soup, "Date")[0]
    close_col_loc = find_column(soup, "Close")[0]

    # Quick access to the header row is stored from find_column() output
    header_row = find_column(soup, "Date")[1]

    # Represents the number of <tr> rows in the parent of the header
    # Will be used to determined how many times to iterate
    num_of_rows = len(header_row.parent.contents)

    for i in range(1, num_of_rows):

        # Quick access to the number of <td> cells in a given row
        cells = header_row.parent.contents[i].contents

        # This is to avoid columns which are used for notes i.e. Dividends
        # given on that date as they may result in out of bounds errors since
        # rows like this have less then available amount of cells than in-
        # tended to parse through.
        if len(cells) > close_col_loc:

            # Focuses on the current 'i' row, retrieves, and prints its date
            # and close information.
            date = header_row.parent.contents[i].contents[date_col_loc]\
                .string
            close = header_row.parent.contents[i].contents[close_col_loc]\
                .string

            print date
            print "Closing Price: %s\n" % close


if __name__ == "__main__":
    main()
