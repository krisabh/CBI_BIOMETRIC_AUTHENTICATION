from database.db_setup import engine, Base

from models import medical, travel, finance, judicial, uidia, aadhar

# Optional: Drop all tables first (for testing)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Tables created successfully!")
