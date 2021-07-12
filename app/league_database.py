import csv
import pickle
from os import path, rename

from app.CurlingLeagueManager import League, TeamMember, Team

"""
Create a class named LeagueDatabase with the following variables and methods.
Note that the load/save functionality can be implemented any way you like but
I recommend using the pickle module.

LeagueDatabase -- a singleton
"""


class LeagueDatabase:
    # Attribute
    _sole_instance = None
    # private variable holding the last id number that was supplied (see methods below)
    _last_oid = None
    # [r/o prop] -- list of the leagues being managed
    leagues = []

    # Constructor
    def __init__(self):
        if LeagueDatabase._sole_instance is None:
            self._last_oid = 0
            self.leagues = []
            LeagueDatabase._sole_instance = self
        else:
            raise Exception("You can't' create two LeagueDatabase classes")

    #  returns the sole instance of this database, creating one if it doesn't exist yet
    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
            cls._last_oid = 0
            cls.leagues = []
        return cls._sole_instance

    """ 
    Loads a LeagueDatabase from the specified file and stores it in _sole_instance.  
    If file_name does not exist or an error occurs when reading it, 
    display a console message 
    (ugh, sorry, it would be better to use the logging framework here but I don't want to go into it) 
    and load the file from the backup (if it exists).  
    
    See save() for information on the backup file.
    """

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode='rb') as f:
                cls._sole_instance = pickle.load(f)
                f.close()
        except FileNotFoundError as e:
            print("ugh, sorry, it would be better to use the logging framework here but I don't want to go into it")

    # add the specified league to the leagues list
    def add_league(self, le):
        self.leagues.append(le)

    # increment _last_id and return its new value (used to generate oid's for your objects)
    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    # save this database on the specified file. Before saving, check if the file exists and if it does,
    # rename it to file_name with ".backup" added.
    def save(self, file_name):
        try:
            if path.exists(file_name):
                rename(file_name, file_name + ".backup")
            with open(file_name, mode='xb') as f:
                pickle.dump(self, f)
                print(f)
                f.close()
        except (FileNotFoundError, FileExistsError) as e:
            print("ugh, sorry, it would be better to use the logging framework here but I don't want to go into it")

    """
    Load a league from a CSV formatted file. 
    (The Python standard library has a nice CSV module (Links to an external site.)).  
    The file will contain three columns: team name, team member name, email.  
    The first line of the file will be a "header" line and should be ignored.  
    The file will be UTF-8 encoded and may contain non-ASCII text.  
    Add this loaded league to the list of leagues.  If an error occurs while loading a league, 
    display a message on the console.
    """

    def import_league(self, league_name, file_name):
        try:
            with open(file_name, newline='') as infile:
                league_in = League(self.next_oid(), league_name)
                reader = csv.reader(infile, delimiter=',')
                next(reader, None)  # skip the headers
                for row in reader:
                    li = list(row)
                    name = li[0]
                    member = li[1]
                    email = li[2]
                    tm = TeamMember(self.next_oid(), member, email)
                    t = Team(self.next_oid(), name)
                    t.add_member(tm)
                    league_in.add_team(t)
                    self.leagues.append(league_in)
        except (FileNotFoundError, FileExistsError) as e:
            print("ugh, sorry, it would be better to use the logging framework here but I don't want to go into it")
            # Check league here
            # for l in self.leagues:
            #    for team in l.teams:
            #        print(team.name)
            #        for member in team.members:
            #            print(member)

    """             
    Write the specified league to a CSV formatted file.  
    The first line of the file must be a "header" row containing the following text (without the leading spaces):
    Team name, Member name, Member email
    If an error occurs while writing a league, display a message on the console.
    """

    def export_league(self, league, file_name):
        fields = ['Team_name', 'Member_name', 'Member_email']
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile, delimiter=',')
                writer.writerow(fields)
                for l in self.leagues:
                    if l.name == league:
                        for team in l.teams:
                            tn = team.name
                            for member in team.members:
                                tup = (tn, member._name, member._email)
                                # tup = tuple([(tn, member._name, member._email) for member in team.members])
                                writer.writerow(tup)
                    else:
                        print("league not found in database")
        except (FileNotFoundError, FileExistsError) as e:
            print("ugh, sorry, it would be better to use the logging framework here but I don't want to go into it")


# main method for testing
if __name__ == "__main__":
    db1 = LeagueDatabase()
    league = League(db1.next_oid(), "Summer21")
    t1 = Team(1, "Busters")
    t2 = Team(2, "Zips")
    tm1 = TeamMember(1, "Fred", "fred@test.com")
    tm2 = TeamMember(2, "Barney", "barney@test.com")
    tm3 = TeamMember(3, "Wilma", "wilma@fakemailz.com")
    t1.add_member(tm1)
    t1.add_member(tm2)
    t2.add_member(tm3)
    league.add_team(t1)
    league.add_team(t2)
    db1.add_league(league)
    db1.save('testdb.dat')
    # db1 = LeagueDatabase()
    db1.load('testdb.dat')
    print(db1.leagues)
    db1.import_league('Summer21', 'test_database2.csv')
    db1.export_league('Summer21', 'test_outdb.csv')
