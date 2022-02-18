from datetime import datetime
import inquirer
from calendar import monthrange


class LogDatePicker:
    current_year = int(datetime.now().strftime('%Y'))
    current_month = int(datetime.now().strftime('%m'))
    current_date = int(datetime.now().strftime('%d'))

    def createYearQuestion(self):
        raw_choices = [self.current_year, self.current_year+1]
        questions = [inquirer.List('Year',
                                   message="Which YEAR do you want report for?",
                                   choices=raw_choices,
                                   )]
        return inquirer.prompt(questions)['Year']

    def createMonthQuestion(self):
        raw_choices = [self.current_month-1,
                       self.current_month, self.current_month+1]
        questions = [inquirer.List('Month',
                                   message="Which MONTH do you want report for?",
                                   choices=raw_choices,
                                   )]
        return inquirer.prompt(questions)['Month']

    def createDayQuestion(self, year, month):
        days_range = monthrange(year, month)
        questions = [inquirer.List('Day',
                                   message="Which DAY do you want report for?",
                                   choices=range(1, days_range[1]+1),
                                   )]
        return inquirer.prompt(questions)['Day']

    def createDefaultQuestion(self):
        raw_choices = [
            'Yes', 'Quick Pick: Choose from a few days back', 'No, pick another date']
        questions = [inquirer.List('Today',
                                   message="Do you want today's report?",
                                   choices=raw_choices,
                                   )]
        return inquirer.prompt(questions)['Today']

    def createFormattedDate(self, year, month, day):
        return '{}-{}-{}'.format(
            year, month, day
        )

    def generateFullPrompt(self):
        main = self.createDefaultQuestion()
        if 'Yes' in main:
            return self.createFormattedDate(
                self.current_year, self.current_month, self.current_date)

        elif 'Quick' in main:
            raw_choices = []
            for i in range(self.current_date-7, self.current_date):
                raw_choices.append(
                    self.createFormattedDate(
                        self.current_year, self.current_month, i
                    ))

            questions = [inquirer.List('Date',
                                       message="Here is a plethora of choices, my Lord!",
                                       choices=raw_choices,
                                       )]
            return inquirer.prompt(questions)['Date']

        else:
            year = self.createYearQuestion()
            month = self.createMonthQuestion()
            day = self.createDayQuestion(year, month)

            return self.createFormattedDate(year, month, day)
