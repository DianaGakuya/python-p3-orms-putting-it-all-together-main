import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        # Create the 'dogs' table if it doesn't exist
        sql = """
            CREATE TABLE IF NOT EXISTS dogs(
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """

        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        # Drop the 'dogs' table if it exists
        sql = """
        DROP TABLE IF EXISTS dogs
        """

        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        # Insert a new dog record into the 'dogs' table and update the object's id
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        # Create a new dog instance, save it to the database, and return the instance
        dog = Dog(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        # Create a new dog instance from a database row
        dog = cls(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

        return dog

    @classmethod
    def get_all(cls):
        # Retrieve all dogs from the 'dogs' table and return a list of instances
        sql = """
            SELECT * FROM dogs
        """

        return [cls.new_from_db(row) for row in CURSOR.execute(sql).fetchall()]

    @classmethod
    def find_by_name(cls, name):
        # Retrieve a dog by name from the 'dogs' table and return an instance
        sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name,)).fetchone()
        if not row:
            return None
        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    @classmethod
    def find_by_id(cls, id):
        # Retrieve a dog by ID from the 'dogs' table and return an instance
        sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row: 
            return None
        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    @classmethod
    def find_or_create_by(cls, name=None, breed=None):
        # Retrieve or create a dog by name and breed in the 'dogs' table and return an instance
        sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """

        row = CURSOR.execute(sql, (name, breed)).fetchone()
        if not row:
            # If the dog doesn't exist, create a new record
            sql = """
                INSERT INTO dogs (name, breed)
                VALUES (?, ?)
            """

            CURSOR.execute(sql, (name, breed))
            return Dog(
                name=name,
                breed=breed,
                id=CURSOR.lastrowid
            )

        # If the dog already exists, return the existing record
        return Dog(
            name=row[1],
            breed=row[2],
            id=row[0]
        )

    def update(self):
        # Update the information of a dog in the 'dogs' table
        sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

# Example Usage:
# Dog.create_table()  # Create the 'dogs' table
# Dog.create("Buddy", "Golden Retriever")  # Create a new dog and save to the database
# all_dogs = Dog.get_all()  # Get all dogs from the database
# Dog.find_by_name("Buddy")  # Find a dog by name
# Dog.find_or_create_by("Rex", "German Shepherd")  # Find or create a dog by name and breed
# Dog.drop_table()  # Drop the 'dogs' table
