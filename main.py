import sys
import time
import logging
from moodleapi import MoodleAPI
from dhis2api import check_pivot_table_favorites
from utils import get_id_prompt

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(levelname)s %(asctime)s :%(message)s', level=logging.INFO)

api = MoodleAPI()


assignment_id = None

if len(sys.argv) > 1:
    assignment_id = int(sys.argv[1])
else:
    course_id = get_id_prompt(api.get_courses(), name_field='displayname')
    assignment_id = get_id_prompt(
        api.get_assignments(course_id), name_field='name')
    help_text = '''
            Next time, to use this same configuration, run as "python {} {}"
        '''.format(sys.argv[0], assignment_id)

    print(help_text)


while True:
    users = api.get_assignment_submitted_users(assignment_id)
    logger.info("Got Submitters:" + str([u['email'] for u in users]))

    submission_texts = [u['submission_text'] for u in users]
    logger.info("Checking submission favorites: " + str(submission_texts))

    valid_texts = check_pivot_table_favorites(submission_texts)
    logger.info("Valid submissions: " + str(valid_texts))

    valid_users = [u for u in users if u['submission_text'] in valid_texts]
    logger.info("Grading users:" + str([u['email'] for u in valid_users]))

    api.save_grades(assignment_id, valid_users)
    logger.info("Sleeping for 60s")
    time.sleep(60)
