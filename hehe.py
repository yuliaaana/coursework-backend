from app import app, db, User, bcrypt

with app.app_context():
    hashed_password = bcrypt.generate_password_hash("1234").decode('utf-8')
    new_user = User(username="xexe2", email="xexe2@gmail.com", password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    print("User added successfully!")


'''import os
secret_key = os.urandom(24)
print(secret_key)
print(secret_key.hex())'''