from bs4 import BeautifulSoup
import urllib2

__author__ = 'Patrick Abejar'


'''This script takes a response from the wunderground.com website and parses
through data in order to find the forecasted or actual temperatures for all
the days in the month of November 2015 if available. This will be printed
to users' screens.
'''


def main():

    print "The following information displays measured and forecasted temp" \
          "eratures for the month of November 2015 in NYC as per the Weath" \
          "er Underground.\n"

    # Take a request from the wunderground.com website in order to receive the
    # temperatures for a given month as HTML data in a response. (It is in-
    # teresting to note that one can change the date part of the URL and
    # retrieve temperature data for many other months available.)
    req = urllib2.Request("http://www.wunderground.com/history/airport/KNYC"
                          "/2015/11/1/MonthlyCalendar.html")
    res = urllib2.urlopen(req)
    html_doc = res.read()
    soup = BeautifulSoup(html_doc, 'html5lib')

    # <td> tags are the most convenient to search through on this website as
    # they are labeled helpfully.
    list_of_td = soup.find_all('td')

    # Out of all the <td> entries 'entry' in the BeautifulSoup object, find
    # the ones that represent one day. This is where the attribute for td is
    # equal to "day".
    for entry in list_of_td:
        if "class" in entry.attrs and "day" in entry['class']:

            # Within one given day, find the components that make up said day
            # by looking at all the <td> tags again.
            day_record = entry.find_all('td')

            # This will fetch the corresponding DATE where the <td> tags in
            # the larger <td class="day"> have an attribute of "date-link"
            for entry1 in day_record:
                if "class" in entry1.attrs and "date-link" in entry1['class']:

                    # The date is retrieved in text surrounded by <a> tags
                    # with attribute "dateText"
                    a_table = entry1.find_all('a')
                    for entry10 in a_table:
                        if "class" in entry10.attrs and "dateText" in \
                                entry10['class']:
                            date = int(entry10.string)
                            print "Day of the Month: %i" % date

            # This records if one is able to retrieve forecasted or actual
            # temperature data. Temperature data is only retrievable 9-10
            # days into the future for this Weather Underground page.
            data_available = False

            # This will fetch the actual and forecasted TEMPERATURES where the
            # <td> tags in the larger <td class="day"> have an attribute of
            # "value-header"
            for entry2 in day_record:
                if "class" in entry2.attrs and "value-header" in \
                        entry2['class'] and (entry2.string == "Actual:"\
                                             or entry2.string == "Forecast:"):

                    # To obtain BOTH the hot and cold temperatures, a parent
                    # view is required.
                    day_record_temp = entry2.parent

                    # The first record of <td> in the day_record represents if
                    # the temperature values are forecasts or actual measured
                    # data.
                    type_of_temp = day_record_temp.find("td").string[:-1]

                    # Temperature readings are listed between <span> tags that
                    # have the class attribute indicated as high or low,
                    # depending upon if one wanted the high temperature for
                    # that day versus the low temperature.
                    temperature_list = day_record_temp.find_all("span")

                    for entry20 in temperature_list:
                        if "class" in entry20.attrs and "high" in \
                                entry20['class']:
                            print "  %s High: %s" % (type_of_temp,
                                                     entry20.string)
                            data_available = True
                        if "class" in entry20.attrs and "low" in \
                                entry20['class']:
                            print "  %s Low: %s" % (type_of_temp,
                                                    entry20.string)
                            data_available = True

            if data_available is False:
                print "  Too far into the future for a forecast"

            print ""


if __name__ == "__main__":
    main()
