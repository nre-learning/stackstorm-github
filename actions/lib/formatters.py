import re

from st2common.util import isotime

__all__ = [
    'issue_to_dict',
    'pull_to_dict',
    'commit_to_dict',
    'label_to_dict',
    'user_to_dict'
]


def issue_to_dict(issue):
    result = {}

    author = user_to_dict(issue.user)
    assignee = user_to_dict(issue.assignee)
    closed_by = user_to_dict(issue.closed_by)

    if issue.pull_request:
        is_pull_request = True
    else:
        is_pull_request = False

    result['id'] = issue.id
    result['repository'] = issue.repository.name
    result['author'] = author
    result['assign'] = assignee
    result['title'] = issue.title
    result['body'] = issue.body
    result['url'] = issue.html_url
    result['state'] = issue.state
    result['is_pull_request'] = is_pull_request

    if issue.labels:
        labels = [label_to_dict(label) for label in issue.labels]
    else:
        labels = []

    result['labels'] = labels

    # Note: We convert it to a serialize type (string)
    if issue.created_at:
        created_at = isotime.format(issue.created_at)
    else:
        created_at = None

    if issue.closed_at:
        closed_at = isotime.format(issue.closed_at)
    else:
        closed_at = None

    result['created_at'] = created_at
    result['closed_at'] = closed_at
    result['closed_by'] = closed_by
    return result


def pull_to_dict(pull):
    result = {}

    author = user_to_dict(pull.user)
    assignee = user_to_dict(pull.assignee)
    merged_by = user_to_dict(pull.merged_by)

    result['id'] = pull.id
    result['pr_id'] = int(re.sub(r'.*/([0-9]+)(#.*)?', r'\1', pull.html_url))
    result['author'] = author
    result['assign'] = assignee
    result['title'] = pull.title
    result['body'] = pull.body
    result['url'] = pull.html_url
    result['base'] = pull.base.ref
    result['head'] = pull.head.ref
    result['state'] = pull.state
    result['merged'] = pull.merged
    result['mergeable_state'] = pull.mergeable_state
    result['merge_commit_sha'] = pull.merge_commit_sha

    if pull.labels:
        labels = [label_to_dict(label) for label in pull.labels]
    else:
        labels = []

    result['labels'] = labels

    if pull.get_commits():
        commits = [commit_to_dict(commit) for commit in pull.get_commits()]
    else:
        commits = []

    result['commits'] = commits

    # Note: We convert it to a serialize type (string)
    if pull.created_at:
        created_at = isotime.format(pull.created_at)
    else:
        created_at = None

    if pull.closed_at:
        closed_at = isotime.format(pull.closed_at)
    else:
        closed_at = None

    if pull.merged_at:
        merged_at = isotime.format(pull.merged_at)
    else:
        merged_at = None

    result['created_at'] = created_at
    result['closed_at'] = closed_at
    result['merged_at'] = merged_at
    result['merged_by'] = merged_by
    return result


def commit_to_dict(commit):
    result = {}
    result['sha'] = commit.sha
    return result


def label_to_dict(label):
    result = {}

    result['name'] = label.name
    result['color'] = label.color
    result['url'] = label.url
    return result


def user_to_dict(user):
    if not user:
        return None

    result = {}
    result['name'] = user.name
    result['login'] = user.login
    return result


def team_to_dict(team):
    if not team:
        return None

    result = {}
    result['id'] = team.id
    result['name'] = team.name
    result['members_count'] = team.members_count
    return result
