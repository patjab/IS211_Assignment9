from bs4 import BeautifulSoup
import urllib2

__author__ = 'Patrick Abejar'


'''This function will find the column number of a given header title with the
left most column being represented as 0 incremeted by 1 in the rightward dir-
ection. It does this by searching for the given header title for all the
string contents of the <th></th> tags in the soup. Once it has found the app-
licable <th></th> tags, it will determine what order the <th></th> tag is in
the row by taking a look at its parent and iterating through all the children
to determine what order from the left most column contains the header.
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
        if entry.string is not None and \
                        entry.string.lower() == header.lower():

            # When the input header is found, a parent view is obtained in
            # order to search for the <td> cell's position from the first
            # <td> cell (or a.k.a. first parent's child)
            for i in range(0, len(entry.parent.contents)):
                if entry.parent.contents[i] == entry:
                    date_column = i

    # First list item returned is the column position of the header
    # Second list item returned is access to the row of the header
    return date_column


'''This script takes a response from the CBSSports.com website and parses
through data in order to find the top 20 players' names, positions, teams,
and their touchdown score. This will be displayed to users' screen.
'''


def main():

    # Take a request from the cbssports.com website in order to receive the
    # number of touchdowns as HTML data in a response
    req = urllib2.Request("http://www.cbssports.com/nfl/stats/playersort/nfl"
                          "/year-2015-season-regular-category-touchdowns/")
    res = urllib2.urlopen(req)
    html_doc = res.read()
    soup = BeautifulSoup(html_doc, 'html5lib')

    # This list named table contains all the instances of the <a></a> tags in
    # the webpage being parsed. <a></a> tags were chosen as players' names
    # have a link back to their webpage, which is established by <a></a> tags
    table = soup.find_all('a')

    # Finds the column where player, pos, team, and td data are located
    name_column = find_column(soup, "player")
    position_column = find_column(soup, "pos")
    team_column = find_column(soup, "team")
    td_column = find_column(soup, "td")

    print "This script prints out the top 20 players of the NFL by the" \
          " number of touchdowns they have received according\nto the " \
          "cbssports.com website.\n(URL: http://www.cbssports.com/nfl/" \
          "stats/playersort/nfl/year-2015-season-regular-category-touc" \
          "hdowns/)\n"

    counter = 1

    # Finds the players through the subsequent if statement and prints the
    # data to screen.
    for entry in table:

        # Rows with "/nfl/players/playerpage/" in their link are associated
        # with a player from the list of links in table.
        if entry['href'][:24] == "/nfl/players/playerpage/":
            # This has the entire row between the <tr> tags for all infor-
            # mation on the player
            player_record = entry.parent.parent

            # Player information is retrieved based on the information found
            # by using find_column on the player_record.
            player_name = player_record.contents[name_column].string
            player_position = player_record.contents[position_column].string
            player_team = player_record.contents[team_column].string
            player_touchdowns = player_record.contents[td_column].string

            print "Name: %s\n Position: %s\n Team: %s\n Touchdowns: %s\n" % \
                  (player_name, player_position, player_team,
                   player_touchdowns)

            counter += 1

        # Only the top 20 players for touchdowns scored sorted by the website
        # will be displayed
        if counter > 20:
            break


if __name__ == "__main__":
    main()
