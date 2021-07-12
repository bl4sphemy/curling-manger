from module6.identifiedobject import IdentifiedObject
from module6.emailer import Emailer


class League(IdentifiedObject):

    """
    Name: League(IdentifiedObject)
    Desc: Class to hold league teams and competitions. Includes methods to return
    """
    #League Constructor
    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    # Teams getter
    @property
    def teams(self):
        return self._teams
    # Competitions getter
    @property
    def competitions(self):
        return self._competitions

    # Teams setter
    def add_team(self, team):
        self._teams.append(team)

    # Competitions setter
    def add_competition(self, competition):
        self._competitions.append(competition)

    # return a list of all teams for which member plays
    def teams_for_member(self, member):
        return [t for t in self._teams if member in t.members]

    # return a list of all competitions in which team is participating
    def competitions_for_team(self, team):
        return [c for c in self._competitions if team in c._teams_competing]

    # return a list of all competitions in which team is participating
    def competitions_for_member(self, member):
        member_teams = [team for team in self._teams if member in team.members]
        return [c for c in self._competitions if any(x in member_teams for x in c._teams_competing)]

    # return a string like: "League Name: N teams, M competitions"
    def __str__(self):
        return str(self.name + ": " + str(len(self.teams)) + " teams, " + str(len(self._competitions)) + " competitions")


class Team(IdentifiedObject):

    """
    Name: Team(IdentifiedObject)
    Desc: Class to hold teams and their players
    """

    # Teams Constructor
    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._team_members = []

    # list of team members
    @property
    def members(self):
        return self._team_members

    # add members, but ignore request to add team member that is already in members
    def add_member(self, member):
        if member not in self._team_members:
            self._team_members.append(member)

    # remove team member
    def remove_member(self, member):
        if member in self._team_members:
            self._team_members.remove(member)

    # send an email to all members of a team except those whose email address is None
    def send_email(self, emailer, subject, message):
        members_emails = []
        for x in self.members:
            members_emails.append(x._email)

        emailer.send_plain_email(members_emails, subject, message)

    # return a string like the following: "Team Name: N members"
    def __str__(self):
        return str(self.name + ": " + str(len(self.members)) + " members")

class TeamMember(IdentifiedObject):

    """
    Name: TeamMember(IdentifiedObject)
    Desc: Class to hold player and players email information.
    """

    # TeamMember Constructor
    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    @property
    # name getter
    def getname(self):
        #print("This is _name: " + self._name)
        return self._name

    @property
    # email getter
    def getemail(self):
        return self._email

    # name setter
    def name(self, name):
        self._name = name

    # email setter
    def email(self, email):
        self._email = email

    def send_email(self, emailer, subject, message):
        e = Emailer()
        e.send_plain_email([self._email], subject, message)

    # return a string like the following: "Name<Email>"
    def __str__(self):
        return str(self._name + "<" + self._email + ">")

class Competition(IdentifiedObject):

    """
    Name: Competition(IdentifiedObject)
    Desc: Class to hold teams, locations, and date of competitions.
    """

    # Competitions Constructor
    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams_competing = teams
        self.location = location
        self.date_time = datetime

    # teams_competing getter
    @property
    def teams_competing(self):
        return self._teams_competing

    # teams_competing setter
    def teams_competing(self, teams):
        self._teams_competing = teams

    def send_email(self, emailer, subject, message):
        team_members_emails = []
        for x in self._teams_competing:
            for y in x._team_members:
                team_members_emails.append(y._email)
        #print(team_members_emails)
        emailer.send_plain_email(team_members_emails, subject, message)

    # return a string like the following: "Competition at location on date_time with N teams"
    def __str__(self):
        if self.date_time is None:
            return str("Competition at " + self.location + " with " + self._teams_competing + " teams")
        else:
            return str("Competition at " + self.location + " on " + str(self.date_time) + " with " + str(len(self._teams_competing)) + " teams")
