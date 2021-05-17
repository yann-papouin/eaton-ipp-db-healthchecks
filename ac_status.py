import sqlite3
import json
import sys
import os

from datetime import datetime

DB_PATH = "/usr/local/Eaton/IntelligentPowerProtector/db"
DB_FILENAME = "mc2.db"
DEBUG = False


def dict_diff(first_dict, second_dict):
    value = {k: second_dict[k] for k in set(second_dict) - set(first_dict)}
    return value


def check_ac_status():
    database = os.path.join(DB_PATH, DB_FILENAME)
    if os.path.exists(database):
        con = sqlite3.connect(database)

        cur = con.cursor()
        cur.execute("SELECT object, value FROM status")

        vals = dict(cur.fetchall())
        if DEBUG:
            output_filename = "vals_" + datetime.now().strftime("%H_%M_%S") + ".json"
            # Print current values to console
            for key, value in vals.items():
                print(key, value)
            # Write same values to a file for diff
            with open(output_filename, "w") as fp:
                json.dump(vals, fp, indent=4)

        if vals["UPS.PowerSummary.PresentStatus.ACPresent"] == "1":
            res = 0
        else:
            res = 1

        con.close()
    else:
        print(database, "not found")
        res = -1
    return res


if __name__ == "__main__":
    return_code = check_ac_status()
    sys.exit(return_code)
