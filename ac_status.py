#!/usr/bin/env python3

import sqlite3
import json
import sys
import os
import argparse

from datetime import datetime

DEBUG = False


def dict_diff(first_dict, second_dict):
    value = {k: second_dict[k] for k in set(second_dict) - set(first_dict)}
    return value


def check_ac_status(db_path, db_filename):
    database = os.path.join(db_path, db_filename)
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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-path",
        nargs=1,
        metavar=("DB_PATH"),
        help="Database path (eg: /usr/local/Eaton/IntelligentPowerProtector/db)",
        default="/usr/local/Eaton/IntelligentPowerProtector/db",
    )
    parser.add_argument(
        "--db-filename",
        nargs=1,
        metavar=("DB_FILENAME"),
        help="Database filename (eg: mc2.db)",
        default="mc2.db",
    )
    args = parser.parse_args(sys.argv[1:])

    return_code = check_ac_status(args.db_path, args.db_filename)
    sys.exit(return_code)
