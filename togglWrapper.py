import base64, datetime, json, logging, math, requests, sys

class DetailedReport:
    @staticmethod
    def __fetch_detailed_report__(user, password, user_agent, workspace_id, since, until, page):
        base_url = 'https://toggl.com/reports/api/v2/details'
        url = base_url +\
            ('?user_agent=' + user_agent if user_agent else '?user_agent=python') +\
            '&workspace_id=' + workspace_id +\
            ('&since=' + since if since else '') +\
            ('&until=' + until if until else '') +\
            ('&page=' + str(page) if page else '')
        auth_decoded = user + ':' + password
        auth_encoded = str(base64.b64encode(auth_decoded.encode('utf-8')), 'utf-8')
        payload = {}
        headers = {
        'Content-Type': 'application/json',
        'Authorization': ('Basic ' + auth_encoded)
        }
        response = requests.request('GET', url, headers=headers, data = payload)
        return json.loads(response.text)
    
    @staticmethod
    def __compile_detailed_report__(user, password, user_agent, workspace_id, since, until):
        print('Compiling...')
        full_response = {}
        first_response = DetailedReport.__fetch_detailed_report__(user, password, user_agent, workspace_id, since, until, 1)
        print('Fetched first page.')
        full_response.update(first_response)
        total_count = full_response['total_count']
        per_page = full_response['per_page']
        pages = math.ceil(total_count/per_page)
        print('Total of {} pages to fetch.'.format(pages))
        for n in range(2, pages + 1):
            print('Fetching page {} of {}...'.format(n, pages))
            next_response = DetailedReport.__fetch_detailed_report__(user, password, user_agent, workspace_id, since, until, n)
            data = full_response['data']
            for item in next_response['data']:
                data.append(item)
            full_response['data'] = data
        print('Finished compiling.')
        return full_response
    
    @staticmethod
    def __default_range__():
        return (None, None)

    @staticmethod
    def __previous_fortnight__():
        today = datetime.date.today()
        until = today - datetime.timedelta(days = today.weekday() + 1) # previous Sunday
        since = until - datetime.timedelta(days = 13) # Monday of the week before last
        return (since.isoformat(), until.isoformat())
    
    @staticmethod
    def __previous_month__():
        today = datetime.date.today()
        until = today - datetime.timedelta(days = today.day) # last day of previous month
        since = until - datetime.timedelta(days = until.day - 1) # first of previous month
        return (since.isoformat(), until.isoformat())
    
    @staticmethod
    def __manual_range__():
        confirmed = False
        while not confirmed:
            while True:
                print('Please enter start date (in format YYYY-MM-DD):')
                since = input()
                try:
                    datetime.date.fromisoformat(since)
                    break
                except ValueError:
                    print('Invalid input, please try again.')
            while True:
                print('Please enter end date (in format YYYY-MM-DD):')
                until = input()
                try:
                    datetime.date.fromisoformat(until)
                    break
                except ValueError:
                    print('Invalid input, please try again.')
            while True:
                print('You have selected the following range: {} - {}'.format(since, until))
                print('Is this correct? Please type "yes" or "no" and press enter.')
                answer = input()
                if answer == 'yes':
                    confirmed = True
                    break
                elif answer == 'no':
                    break
                else:
                    print('Answer "{}" not recognised. Please try again.'.format(answer))
        return (since, until)
    
    @staticmethod
    def run(user, password, workspace_id):
        try:
            supported_range_modes = ['default', 'fortnightly', 'monthly', 'manual']
            while True:
                print('Please type report range and press enter, or leave blank for default (past week).')
                print('Supported inputs: {}.'.format(', '.join(supported_range_modes)))
                range_mode = input().lower()
                if range_mode == '':
                    range_mode = 'default'
                if (range_mode not in supported_range_modes):
                    print('Input "{}" not supported.'.format(range_mode))
                else:
                    break
            print("Selected mode:", range_mode)
            range_functions = {
                'default': DetailedReport.__default_range__,
                'fortnightly': DetailedReport.__previous_fortnight__,
                'monthly': DetailedReport.__previous_month__,
                'manual': DetailedReport.__manual_range__
            }
            (since, until) = range_functions[range_mode]()
            print('Selected date range {} to {} based on range mode "{}"'.format(since, until, range_mode))
            
            print('Please type desired file name (without extension) where results should be saved and press enter, or leave blank for default ({}.json).'.format(range_mode))
            filename = input()
            if filename == '':
                filename = range_mode
            filename += '.json'
            print('Output file: {}'.format(filename))

            args = {
                'user':user,
                'password':password,
                'user_agent':"TogglWrapper",
                'workspace_id':workspace_id,
                'since':since,
                'until':until,
            }

            result = json.dumps(DetailedReport.__compile_detailed_report__(**args))

            print('Writing to file "{}"...'.format(filename))
            output = open(filename,'w')
            output.write(result)
            output.close()
            print('Finished writing to file.')
        except KeyboardInterrupt:
            print('\rCancelled.')
