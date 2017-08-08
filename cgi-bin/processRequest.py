#!/usr/bin/python3

import cgi, shelve


# Tuples containing input names and printable names.
fieldNames = ('key', 'first_name', 'second_name', 'age', 'genre')
printableNames = ('Key', 'First name', 'Second name', 'Age', 'Genre')
# Path to persistence data.
dbName = 'data/persons_db'

class Person():
    """
    Class to create 'person' objects.
    Stores key (unique id), first name, second name, age and genre.
    """

    def __init__(self, key, firstName, secondName, age, genre):
        self.key = key
        self.firstName = firstName
        self.secondName = secondName
        self.age = age
        self.genre = genre

    def getAllProperties(self):
        properties = (self.key, self.firstName, self.secondName, self.age, self.genre)
        return properties

    def getKey(self):
        return self.key

    def setAllProperties(self, key, firstName, secondName, age, genre):
        self.key = key
        self.firstName = firstName
        self.secondName = secondName
        self.age = age
        self.genre = genre


def processrecord(action, form):
    """
    Checks if key is present.
    Calls fetch or update function.
    Opens and closes shelve database.
    """
    db = shelve.open(dbName)
    if not fieldNames[0] in form:
        print('Fill key in order to upgrade your record!')
        return

    print("Content-type:text/html\n")

    if action == 'fetch':
        fetchRecord(db, form)
    else:
        updateRecord(db, form)

    db.close()


def fetchRecord(db, form):
    """
    Loads person record from the database.
    Returns html table with the informations.
    """
    if form[fieldNames[0]].value in db:
        person = db[form[fieldNames[0]].value]
        properties = person.getAllProperties()
        # Print table with 'for' generated columns.
        print('<table>')
        for i, name in enumerate(printableNames):
            print('<tr><td>' + name + '</td><td>', properties[i], '</td></tr>')
        print('</table>')
    else:
        print('Person with key: ', form[fieldNames[0]].value, "is not in database!")


def updateRecord(db, form):
    """
    Updates person record in database.
    Processes form and saves informations into the database.
    """
    info = {}
    for record in fieldNames:
        if not record in form:
            info[record] = ''
        else:
            info[record] = form[record].value

    person = Person(info[fieldNames[0]], info[fieldNames[1]], info[fieldNames[2]], info[fieldNames[3]],
                    info[fieldNames[4]])

    db[person.getKey()] = person
    print('Record has been updated.')


def main():
    """
    Checks if form contains 'action' field.
    """
    form = cgi.FieldStorage()
    if 'action' in form:
        action = form['action'].value
    else:
        action = None

    if action == 'fetch' or action == 'update':
        processrecord(action, form)
    else:
        print('Bad request!')


if __name__ == '__main__':
    main()
