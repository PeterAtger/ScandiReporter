from datetime import datetime, timedelta
import requests
from calendar import monthrange
from humanfriendly import format_timespan
import pyperclip as pc
import animation
import consts
from log_date_picker import LogDatePicker


class ReportMaker_9000:
    _date = ''

    def _get_date(self, format=consts.GET_DATE_DEFAULT):
        year, month, day = self._date.split('-')
        date_obj = datetime(int(year), int(month), int(day))

        tom = date_obj + \
            timedelta(3) if date_obj.strftime(
                '%a') == 'Fri' else date_obj + timedelta(1)

        tom_year, tom_month, tom_date, tom_day = tom.strftime(
            '%Y'), tom.strftime('%m').replace('0', ''), tom.strftime('%d'), tom.strftime('%A')

        if format == consts.GET_DATE_DEFAULT:
            return self._date
        if format == consts.GET_DATE_LOGGABLE:
            return f'{day}.{month}.{year}'
        if format == consts.GET_DATE_DAY:
            return date_obj.strftime('%A')
        if format == consts.GET_DATE_TOMORROW:
            return f'{tom_day}: {tom_date}.{tom_month}.{tom_year}'

    def _create_report_head(self):
        greeting = "Hello team,\n\n"
        day_log = "Done Today: "
        day_log += '{} : {}\n\n'.format(self._get_date(consts.GET_DATE_DAY),
                                        self._get_date(consts.GET_DATE_LOGGABLE))

        return greeting + day_log

    def _create_report_end(self):
        pending = 'Pending Tasks: {}\n\n'.format(
            self._get_date(format=consts.GET_DATE_TOMORROW))
        regards = "Best Regards, \n"

        return pending + regards

    def _create_report_body(self, response):
        r_json = response
        # r_json = consts.RESPONSE_EXAMPLE
        report_body = ""
        for idx, log in enumerate(r_json['worklog']):
            # Ticket Head
            report_body += '{}. - '.format(idx+1)
            report_body += log['issue']['name']
            report_body += ' - ({})'.format(log['issue']['self'])
            report_body += ' - '
            report_body += format_timespan(log['timeSpentSeconds'])

            # Ticket description
            report_body += '\n'
            report_body += '\t'
            report_body += log['description'].replace('\n', '\n\t')
            report_body += '\n'
            report_body += '\n'

        return(report_body)

    def _generate_response(self, jira):
        date = self._get_date()
        return requests.post(
            url=consts.URL,
            data={
                "jiraDate": date,
                "workspace": jira['workspaceName'],
                "token": jira['token'],
                "jiraWorklogUsername": consts.TEMPO_ID,
                "jiraEmail": "peter.atef@scandiweb.com",
                "atlassianToken": consts.ATLASIAN_TOKEN
            }
        )

    def _combine_jiras(self):
        response_web = self._generate_response(consts.SCANDIWEB).json()
        response_flow = self._generate_response(consts.SCANDIFLOW).json()

        response_combined = response_web
        response_combined['worklog'] += response_flow['worklog']

        return response_combined

    def set_date(self):
        logger = LogDatePicker()
        self._date = logger.generateFullPrompt()

    @animation.wait()
    def create_full_report(self):
        return(
            self._create_report_head()
            + self._create_report_body(response=self._combine_jiras())
            + self._create_report_end()
        )


reporter = ReportMaker_9000()
reporter.set_date()
report = reporter.create_full_report()
pc.copy(report)

print(report)
print('\n\nAlready Copied to clipboard 😉')
