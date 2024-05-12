import re

def add_time(start, duration, daystart = ''):

    # Regular expression
    num_regex = '\d+'
    semi_colon_detect = '[:]+'
    ampm_regex = '[aApP][mM]$'
    week_regex = '[a-zA-Z]+'

    # Week dictionary & list, use to comparison
    week_dict = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    week_comparison = [i.lower() for i in week_dict.values()]

    # Extract all necessary information from start and duration
    start_hour_min = re.findall(num_regex, start)
    duration_hour_min = re.findall(num_regex, duration)
    start_colon = re.findall(semi_colon_detect, start)
    duration_colon = re.findall(semi_colon_detect, duration)
    start_apm = re.findall(ampm_regex, start)
    start_week_day = re.findall(week_regex, daystart)

    start_hour_min_num = [int(i) for i in start_hour_min]
    duration_hour_min_num = [int(i) for i in duration_hour_min]

    # Check the basic condition whether the string from input fail
    if len(start_hour_min) != 2 or len(duration_hour_min) != 2:
        return 'Break! Incorrect time format. Time format must be in hour:min am/pm/AM/PM'
    elif len(start_hour_min[0]) >= 3 or len(start_hour_min[1]) != 2:
        return 'Break! Hour cannot contains 3 or more digits. Minutes must be 2 digits!'
    elif len(duration_hour_min[1]) != 2:
        return 'Break! Minutes must be 2 digits!'

    if len(start_colon) != 1 or len(duration_colon) != 1:
        return 'Break! Incorrect time format. Time format must be in hour:min am/pm/AM/PM'

    if len(start_apm) != 1:
        return 'Break! Incorrect time format. Time format must be in hour:min am/pm/AM/PM'

    if start_hour_min_num[0] >= 13 or start_hour_min_num[0] == 0:
        return 'Break! Hour cannot greater than or equal to 13 plus Hour cannot be zero!'

    if start_hour_min_num[1] >= 60 or duration_hour_min_num[1] >= 60:
        return 'Break! Min should be from 0 to 59!!'

    if len(start_week_day) == 0:
        True

    if len(start_week_day) == 1:
        if start_week_day[0].lower() not in week_comparison:
            return 'Weekday Error!'
    if len(start_week_day) >= 2:
        return 'Weekday Error!'

    ##### Calculation of hour:min
    new_string_comp_dict = {}

    # initialize the am or pm in dictionary
    new_string_comp_dict['APM'] = start_apm[0]

    # AM/PM Transformer, range from 0 to 23
    duration_cycle_canceller = 24 * (duration_hour_min_num[0] // 24)
    duration_hour = duration_hour_min_num[0] - duration_cycle_canceller

    # Initialize the number of day in dictionary by duration hour simplifier
    new_string_comp_dict['day'] = duration_hour_min_num[0] // 24

    # First step simplify the duration hour along with the am pm, making the duration hour range from 0 to 11
    if duration_hour >= 12 and start_apm[0].upper() == 'AM':
        duration_hour -= 12
        new_string_comp_dict['APM'] = 'PM'
    elif duration_hour >= 12 and start_apm[0].upper() == 'PM':
        duration_hour -= 12
        new_string_comp_dict['APM'] = 'AM'
        new_string_comp_dict['day'] += 1

    # special case duration hour is 0, after consider that case, duration hour is within range 1 to 11
    if duration_hour == 0:
        new_string_comp_dict['hour'] = start_hour_min_num[0]
        if start_hour_min_num[1] + duration_hour_min_num[1] >= 60:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1] - 60
            new_string_comp_dict['hour'] += 1
            if new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'AM':
              new_string_comp_dict['APM'] = 'PM'
            elif new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'PM':
              new_string_comp_dict['APM'] = 'AM'
              new_string_comp_dict['day'] += 1
        else:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1]

    # special case start hour is 12, after consider that case, start hour range from 1 to 11
    if start_hour_min_num[0] == 12:
        new_string_comp_dict['hour'] = duration_hour
        if start_hour_min_num[1] + duration_hour_min_num[1] >= 60:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1] - 60
            new_string_comp_dict['hour'] += 1
            if new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'AM':
              new_string_comp_dict['APM'] = 'PM'
            elif new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'PM':
              new_string_comp_dict['APM'] = 'AM'
              new_string_comp_dict['day'] += 1
        else:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1]

    # start hour range from 1 to 11 & duration hour range from 1 to 11
    elif start_hour_min_num[0] <= 11 and duration_hour != 0:
        new_string_comp_dict['hour'] = start_hour_min_num[0]
        if start_hour_min_num[1] + duration_hour_min_num[1] >= 60:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1] - 60
            new_string_comp_dict['hour'] += 1
        else:
            new_string_comp_dict['min'] = start_hour_min_num[1] + duration_hour_min_num[1]

        new_string_comp_dict['hour'] += duration_hour

        if new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'AM':
            new_string_comp_dict['APM'] = 'PM'
        elif new_string_comp_dict['hour'] == 12 and new_string_comp_dict['APM'] == 'PM':
            new_string_comp_dict['APM'] = 'AM'
            new_string_comp_dict['day'] += 1
        elif new_string_comp_dict['hour'] > 12 and new_string_comp_dict['APM'] == 'AM':
             new_string_comp_dict['hour'] -= 12
             new_string_comp_dict['APM'] = 'PM'
        elif new_string_comp_dict['hour'] > 12 and new_string_comp_dict['APM'] == 'PM':
             new_string_comp_dict['hour'] -= 12
             new_string_comp_dict['APM'] = 'AM'
             new_string_comp_dict['day'] += 1

    # change the type of value in dictionary from integer to string
    new_string_comp_dict['hour'] = str(new_string_comp_dict['hour'])
    new_string_comp_dict['min'] = str(new_string_comp_dict['min'])
    new_string_comp_dict['colon'] = start_colon[0]

    # Make the single digit case in minute of dictionary to double digit
    if len(new_string_comp_dict['min']) == 1:
        new_string_comp_dict['min'] = '0' + new_string_comp_dict['min']

    # return the require answer
    if len(start_week_day) != 0:
        week_index = week_comparison.index(start_week_day[0].lower())
        shift_result_weekday = week_dict[(week_index + new_string_comp_dict['day']) % 7]

        if new_string_comp_dict['day'] == 0:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM'] + ', ' + shift_result_weekday

        elif new_string_comp_dict['day'] == 1:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM'] + ', ' + shift_result_weekday + ' ' + '(next day)'

        elif new_string_comp_dict['day'] > 1:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM'] + ', ' + shift_result_weekday + f' ({new_string_comp_dict["day"]} days later)'

    else:
        if new_string_comp_dict['day'] == 0:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM']


        elif new_string_comp_dict['day'] == 1:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM'] + ' ' + '(next day)'

        elif new_string_comp_dict['day'] > 1:
            return '' + new_string_comp_dict['hour'] + new_string_comp_dict['colon'] + new_string_comp_dict['min'] + ' ' + new_string_comp_dict['APM'] + f' ({new_string_comp_dict["day"]} days later)'
