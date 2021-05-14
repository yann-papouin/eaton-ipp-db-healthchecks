import sqlite3
import json


def dict_diff(first_dict, second_dict):
    value = {k: second_dict[k] for k in set(second_dict) - set(first_dict)}
    return value


if __name__ == "__main__":
    con = sqlite3.connect("mc2.db")

    cur = con.cursor()
    cur.execute("SELECT object, value FROM status")

    vals = dict(cur.fetchall())
    for key, value in vals.items():
        print(key, value)

    with open('vals.json', 'w') as fp:
        json.dump(vals, fp,  indent=4)

    con.close()
