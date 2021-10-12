from datetime import date

import pandas


def dates_between_two_dates(start_date, end_date, frequency='m', complete_period=True):
    """
    Returns a list of dates between period of time.
    :param start_date:
    :param end_date:
    :param frequency:
    :param complete_period:
    :return: list of dates between start and end date.
    """
    year1 = None
    month1 = None
    day1 = None
    year2 = None
    month2 = None
    day2 = None
    if '/' in start_date:
        year1 = str(start_date).split('/')[2]
        month1 = str(start_date).split('/')[1]
        day1 = str(start_date).split('/')[0]

        year2 = str(end_date).split('/')[2]
        month2 = str(end_date).split('/')[1]
        day2 = str(end_date).split('/')[0]


    elif '-' in start_date:
        year1 = str(start_date).split('-')[2]
        month1 = str(start_date).split('-')[1]
        day1 = str(start_date).split('-')[0]

        year2 = str(end_date).split('-')[2]
        month2 = str(end_date).split('-')[1]
        day2 = str(end_date).split('-')[0]

    list_official_dates = [date(int(year1), int(month1), int(day1))]

    sdate = date(int(year1), int(month1), int(day1))  # start date
    edate = date(int(year2), int(month2), int(day2))  # end date
    dates = pandas.date_range(sdate, edate, freq=frequency, normalize=True)


    for i in range(len(dates)):
        list_official_dates.append(dates[i])

    list_official_dates.append(date(int(year2), int(month2), int(day2)))


    for i in range(len(list_official_dates)):
        list_official_dates[i] = str(list_official_dates[i]).replace(' 00:00:00', '')


    return list_official_dates


if __name__ == '__main__':
    dates_between_two_dates(start_date='01/01/2020', end_date='02/09/2020', frequency='d',
                            complete_period=True)
