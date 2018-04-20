# moodle_dhis2_assign_grader
A Python tool that checks against DHIS2 API to grade assignments in Moodle

## Configuration and Usage
1. Create a webservice token in Moodle (see [docs](https://docs.moodle.org/33/en/Using_web_services) with the following functions enabled:

```php
core_course_get_courses
core_user_get_users_by_field
mod_assign_get_assignments  
mod_assign_get_submissions
```

2. Update `config.py` with your configuration:

```python
DHIS2_URL = "https://play.dhis2.org/2.29"
DHIS2_USERNAME = "admin"
DHIS2_PASSWORD = "district"

MOODLE_KEY = '<YOUR_MOODLE_WEB_SERVICE_TOKEN>'
MOODLE_URL = "http://example.com/"

```
3. Create an assignment in Moodle with "submission type" as "Online text" as 
shown in the screenshot below:

![Image of Assignment](https://github.com/aatishnn/moodle_dhis2_assign_grader/blob/master/img/assignment.png)


4. Run `main.py`

Every 60s, it checks submissions and checks it against DHIS2 favorites. If matching favorites are found, it grades users' ubmission with 100 marks.

### Sample Run
```bash
➜ python main.py
1: asd
2: Course restoration in progress
3: Course restoration in progress copy 1
4: ★Master Course (5 days)
Enter ID:4
1: Assignment(Data Entry, Validation Report)
2: Assignment(Dataset Report, Reporting Rate Summary)
3: Assignment(Pivot Table)
4: Assignment(Data Visualizer)
5: Assignment(Final Practice)
6: Pivot Tables Assignment
Enter ID:6

            Next time, to use this same configuration, run as "python main.py 6"
        
INFO 2018-04-20 20:27:04,557 :Got Submitters:['<REDACTED>', '<REDACTED>']
INFO 2018-04-20 20:27:04,557 :Checking submission favorites: ['asf', 'pivot_tables_test']
INFO 2018-04-20 20:27:05,559 :Valid submissions: ['asf']
INFO 2018-04-20 20:27:05,559 :Grading users:['<REDACTED>']
INFO 2018-04-20 20:27:05,636 :Sleeping for 60s
```
