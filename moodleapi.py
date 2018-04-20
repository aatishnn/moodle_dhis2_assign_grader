import requests
import re

from config import MOODLE_URL, MOODLE_ENDPOINT, MOODLE_KEY


def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.

    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict is None:
        out_dict = {}

    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def remove_html(text):
    """Remove html tags from a string and strips it"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()


class MoodleAPI(object):
    def __init__(self):
        pass

    def call(self, fname, **kwargs):
        """Calls moodle API function with function name fname and keyword arguments.
        Example:
        >>> call_mdl_function(
        'core_course_update_courses',courses=[
            {'id':1, 'fullname': 'My favorite course'}
        ])
        """
        parameters = rest_api_parameters(kwargs)
        parameters.update({
            "wstoken": MOODLE_KEY,
            'moodlewsrestformat': 'json',
            "wsfunction": fname
        })
        response = requests.post(MOODLE_URL + MOODLE_ENDPOINT, parameters)
        response.raise_for_status()
        return response.json()

    def get_courses(self):
        courses = self.call('core_course_get_courses')
        return courses

    def get_feedbacks(self, course_id):
        return self.call(
            'mod_feedback_get_feedbacks_by_courses',
            courseids=[course_id])['feedbacks']

    def get_questions(self, feedback_id):
        return self.call(
            'mod_feedback_get_items',
            feedbackid=feedback_id)['items']

    def get_responses(self, feedback_id):
        return self.call(
            'mod_feedback_get_responses_analysis',
            feedbackid=feedback_id)['attempts']

    def get_assignments(self, course_id):
        return self.call(
            'mod_assign_get_assignments',
            courseids=[course_id],
            includenotenrolledcourses=1)['courses'][0]['assignments']

    def get_submissions(self, assignment_id):
        return self.call(
            'mod_assign_get_submissions',
            assignmentids=[assignment_id],
            status='submitted')['assignments'][0]['submissions']

    def get_users_by_field(self, values, field='id'):
        return self.call(
            'core_user_get_users_by_field',
            field=field,
            values=values
        )

    def get_assignment_submitted_users(self, assignment_id):
        submissions = self.get_submissions(assignment_id)
        user_ids = []
        user_submissions = []
        for submission in submissions:
            user_ids.append(submission['userid'])
            user_submissions.append({
                'userid': submission['userid'],
                'submission_text': remove_html(
                    submission['plugins'][0]['editorfields'][0]['text'])
            })
        users = self.get_users_by_field(user_ids)
        for user in users:
            user['submission_text'] = next(
                d for d in user_submissions if d['userid'] == user['id']
            )['submission_text']
        return users

    def save_grades(self, assignmentid, users):
        grades = []
        for user in users:
            grades.append({
                'userid': user['id'],
                'grade': 50.0,
                'attemptnumber': -1,
                'addattempt': 0,
                'workflowstate': 'Released'
            })
        self.call(
            'mod_assign_save_grades',
            assignmentid=assignmentid,
            applytoall=0,
            grades=grades
        )
