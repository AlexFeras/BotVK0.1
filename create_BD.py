def insert(t):
    s.add(t)
    s.commit()
def delete(uid):
    s.query(Item).filter(Item.id == uid).delete()
    s.commit()
def change(uid, team):
    t = s.query(Item).filter(Item.id == uid).delete().first()
    t.team = team
    s.commit


