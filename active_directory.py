'''Module contains Group class used for managing active directory.'''
import json

class Group:
    def __init__(self, name):
        self._name = name
        self._groups = []
        self._users = []

    @property
    def groups(self):
        return self._groups

    @property
    def users(self):
        return self._users

    @property
    def name(self):
        return self._name

    @property
    def all_groups(self):
        return self._get_groups(self)

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def extend_groups(self, groups):
        self.groups.extend(groups)

    def extend_users(self, users):
        self.users.extend(users)

    def _get_groups(self, group):
        groups = {}
        groups['name'] = group.name
        groups['users'] = group.users
        groups['children'] = [g._get_groups(g) for g in group.groups]
        return groups

    def __contains__(self, user):
        return ((user in self.users)
                or any(group.__contains__(user) for group in self.groups))

    def __str__(self):
        return json.dumps(self.all_groups, indent=4)
