import database

basel_id = 20221502065
yazan_id = 20222502096


db = database.Database()


# db.update_comunities_membership(basel_id, AAAI = True)

data = db.get_comunity_members(AAAI=True)
print(data)

# db.delete_students()

# db.insert_rows_from_sheets()

# db.make_admin(20221502065, database.Roles.VICE_PRESIDENT)

db.close()