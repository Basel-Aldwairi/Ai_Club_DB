from src import database

db = database.Database()

student_roles = [
    (20221502065, database.Roles.VICE_PRESIDENT), # Basel vp lead
    (20222502096, database.Roles.PRESIDENT), # Yazan pres lead
    (20231702004, database.Roles.SECRETARY), # Sarah secertary lead
    (20241103013, database.Roles.PR_TEAM), # Hala pr lead
    (20241103024, database.Roles.PR_TEAM), # Zaid Rashdan pr
    (20221102027, database.Roles.RESEARCH_TEAM), # Ramez research lead
    (20229102061, database.Roles.RESEARCH_TEAM), # Farah research
    (20231504016, database.Roles.PR_TEAM),
    # Ghasan Technical lead
    # Adam Technical
    # Hashem Finance lead
    # Profs
]


for sr in student_roles:
    db.update_role(sr[0], sr[1])

db.close()