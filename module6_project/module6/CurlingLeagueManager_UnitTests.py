from CurlingLeagueManager import Team
from CurlingLeagueManager import TeamMember
from CurlingLeagueManager import Competition
from CurlingLeagueManager import League
from emailer import Emailer

import unittest
import datetime


class TeamMemberTests(unittest.TestCase):
    def test_create(self):
        oid = 1
        name = "Fred"
        email = "fred.flintstone@gmail.com"
        tm = TeamMember(oid, name, email)
        self.assertEqual(oid, tm.oid)
        self.assertEqual(name, tm._name)
        self.assertEqual(email, tm._email)

    def test_equality_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # team members must be equal to themselves
        self.assertTrue(tm_1 == tm_1)
        self.assertTrue(tm_2 == tm_2)
        self.assertTrue(tm_3 == tm_3)

        # same id are equal, even if other fields different
        self.assertTrue(tm_1 == tm_2)

        # different ids are not equal, even if other fields the same
        self.assertTrue(tm_1 != tm_3)

    def test_hash_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # hash depends only on id
        self.assertTrue(hash(tm_1) == hash(tm_2))

        # objects with different id's may have different hash codes
        # note: this is not a requirement of the hash function but
        # for the case of id == 1 and id == 2 we can verify that their
        # hash codes are different in a REPL (just print(hash(1)) etc).
        self.assertTrue(hash(tm_1) != hash(tm_3))

    def test__str__(self):
        tm_1 = TeamMember(1, "name", "email")
        self.assertEqual(tm_1.__str__(), 'name<email>')


class TeamTests(unittest.TestCase):
    def test_create(self):
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        self.assertEqual(name, t.name)
        self.assertEqual(oid, t.oid)

    def test_adding_adds_to_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)
        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    def test_removing_removes_from_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        t.remove_member(tm1)
        self.assertNotIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    def test_send_email(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_1.email("blah")
        #tm_1.send_email("sender1@gmail.com"], "hello", "do you like coffee?")

    def test__str__(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "g")
        t.add_member(tm1)
        self.assertEqual(t.__str__(), 'Flintstones: 1 members')


class CompetitionTests(unittest.TestCase):
    def test_create(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "There", now)

        self.assertEqual("Here", c1.location)
        self.assertEqual(1, c1.oid)
        self.assertIsNone(c1.date_time)
        self.assertEqual(2, len(c1._teams_competing))
        self.assertIn(t1, c1._teams_competing)
        self.assertIn(t2, c1._teams_competing)
        self.assertNotIn(t3, c1._teams_competing)

        self.assertEqual("There", c2.location)
        self.assertEqual(2, c2.oid)
        self.assertEqual(now, c2.date_time)
        self.assertEqual(2, len(c2._teams_competing))
        self.assertNotIn(t1, c2._teams_competing)
        self.assertIn(t2, c2._teams_competing)
        self.assertIn(t3, c2._teams_competing)

    def test_send_email(self):
        now = "date"
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        c1 = Competition(1, [t1, t2], "Here", now)
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Wilma", "wilma")
        t1.add_member(tm1)
        t2.add_member(tm2)
        e = Emailer()
        e.configure("me@email.com")
        c1.send_email(e, "Hello", "Testing Emails")


    def test__str__(self):
        now = "date"
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        c1 = Competition(1, [t1, t2], "Here", now)
        self.assertEqual(c1.__str__(), 'Competition at Here on date with 2 teams')

class LeagueTests(unittest.TestCase):
    def test_create(self):
        league = League(1, "AL State Curling League")
        self.assertEqual(1, league.oid)
        self.assertEqual("AL State Curling League", league.name)
        self.assertEqual([], league.teams)
        self.assertEqual([], league.competitions)

    def test_adding_team_adds_to_teams(self):
        t = Team(1, "Ice Maniacs")
        league = League(1, "AL State Curling League")
        self.assertNotIn(t, league.teams)
        league.add_team(t)
        self.assertIn(t, league.teams)

    def test_adding_competition_adds_to_competitions(self):
        c = Competition(1, [], "Local tourney", None)
        league = League(13, "AL State Curling League")
        self.assertNotIn(c, league.competitions)
        league.add_competition(c)
        self.assertIn(c, league.competitions)

    @staticmethod
    def build_league():
        league = League(1, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        all_teams = [t1, t2, t3]
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Barney", "barney")
        tm3 = TeamMember(3, "Wilma", "wilma")
        tm4 = TeamMember(4, "Betty", "betty")
        tm5 = TeamMember(5, "Pebbles", "pebbles")
        tm6 = TeamMember(6, "Bamm-Bamm", "bam-bam")
        tm7 = TeamMember(7, "Dino", "dino")
        tm8 = TeamMember(8, "Mr. Slate", "mrslate")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        t2.add_member(tm5)
        t3.add_member(tm6)
        t3.add_member(tm7)
        t3.add_member(tm8)
        # every team plays every other team twice
        oid = 1
        for c in [Competition(oid := oid + 1, [team1, team2], team1.name + " vs " + team2.name, None)
                  for team1 in all_teams
                  for team2 in all_teams
                  if team1 != team2]:
            league.add_competition(c)
        return league

    def test_big_league(self):
        league = self.build_league()
        t = league.teams[0]
        cs = league.competitions_for_team(t)
        # matchups are (t1, t2), (t1, t3), (t2, t1), (t3, t1) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t1 vs t2", "t1 vs t3", "t2 vs t1", "t3 vs t1"}, cs_names)

        self.assertEqual([league.teams[2]], league.teams_for_member(league.teams[2].members[0]))

        # Grab a player from the third team
        cs = league.competitions_for_member(league.teams[2].members[0])
        # matchups are (t3, t1), (t3, t2), (t2, t3), (t1, t3) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehensionq
        self.assertEqual({"t3 vs t1", "t3 vs t2", "t2 vs t3", "t1 vs t3"}, cs_names)

    def test__str__(self):
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        league = League(1, "AL State Curling League")
        league.add_team(t1)
        league.add_team(t2)
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Barney", "barney")
        tm3 = TeamMember(3, "Wilma", "wilma")
        tm4 = TeamMember(4, "Betty", "betty")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        self.assertEqual(league.__str__(), 'AL State Curling League: 2 teams, 0 competitions')
