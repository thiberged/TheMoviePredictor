import mysql.connector
import sys
import argparse
import csv

def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {}").format(table, id)

def findAllQuery(table):
    return ("SELECT * FROM {}").format(table)

def find(table, id, search):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    if search == 'list':
        cursor.execute(findAllQuery(table))
    if search == 'find':
        cursor.execute(findQuery(table, id))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

parser = argparse.ArgumentParser(prog='app.py')

parser.add_argument('context', choices=['people', 'movies'], help='le contexte dans le quel nous allons travailler')
subparsers = parser.add_subparsers(dest='action', required=True)

parser_list = subparsers.add_parser('list')
parser_list.add_argument('--export', metavar='fichier.csv')

parser_find = subparsers.add_parser('find')
parser_find.add_argument('id', metavar='id', type=int)

args = parser.parse_args()

# arguments = sys.argv
# arguments.pop(0)

if args.context == "people":
    if args.action == "find":
        peopleId = args.id
        results = find("people", peopleId, 'find')
        if args.export:
            print('exportation')
            csvfile = open(args.export, 'w', encoding='utf-8', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(results[0].keys())
            for person in results:
                writer.writerow(person.values())
            csvfile.close
        else:
            for person in results:
                print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))
    if args.action == "list":
        results = find("people", 0, 'list')
        if args.export:
            print('exportation')
            csvfile = open(args.export, 'w', encoding='utf-8', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(results[0].keys())
            for person in results:
                writer.writerow(person.values())
            csvfile.close()
        else:
            for person in results:
                print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))

if args.context == "movies":
    if args.action == "find":
        movieId = args.id
        results = find("movies", movieId, 'find')
        if args.export:
            print('exportation')
            csvfile = open(args.export, 'w', encoding='utf-8', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(results[0].keys())
            for movie in results:
                writer.writerow(movie.values())
            csvfile.close()
        else:
            for movie in results:
                print("#{}: {} {} {} {} {} {} {} {} {}"
                .format(movie['id'], movie['tittle'], movie['original_tittle'], movie['rating'], movie['production_budget'],
                movie['marketing_budget'], movie['duration'], movie['release_date'], movie['3d'], movie['synopsis']))
    if args.action == "list":
        results = find("movies", 0, 'list')
        if args.export:
            print('exportation')
            csvfile = open(args.export, 'w', encoding='utf-8', newline='')
            writer = csv.writer(csvfile)
            writer.writerow(results[0].keys())
            for movie in results:
                writer.writerow(movie.values())
            csvfile.close()
        else:
            for movie in results:
                print("#{}: {} {} {} {} {} {} {} {} {}"
                .format(movie['id'], movie['tittle'], movie['original_tittle'], movie['rating'], movie['production_budget'],
                movie['marketing_budget'], movie['duration'], movie['release_date'], movie['3d'], movie['synopsis']))

