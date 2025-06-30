#!/usr/bin/env python3

import sqlite3
import json
import sys
import os
import argparse

from datetime import datetime

DEBUG = True


def dict_diff(first_dict, second_dict):
    value = {k: second_dict[k] for k in set(second_dict) - set(first_dict)}
    return value


def try_run_error_cmd(on_error_cmd):
    if on_error_cmd:
        print("Run", on_error_cmd)
        os.system(on_error_cmd)

def check_ac_status(db_path, db_filename, on_error_cmd):
    database = os.path.join(db_path, db_filename)
    if os.path.exists(database):
        con = sqlite3.connect(database)

        cur = con.cursor()
        try:
            cur.execute("SELECT object, value FROM status")
            vals = dict(cur.fetchall())
            cur.close()
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

            if res == 0 and vals["System.CommunicationLost"] == "1":
                com_error_state = vals.get("System.CommunicationErrorState")
                print("----------------------------------------------")
                print(f"Communication Lost: {com_error_state}\n")
                print("Check that USB auto suspend is disabled on your Proxmox Host:")
                print('GRUB_CMDLINE_LINUX_DEFAULT="quiet usbcore.autosuspend=-1"')
                print("----------------------------------------------")
                res = 2

        except sqlite3.OperationalError as e:
            print(e.args[0])
            if e.args[0] == "database is locked":
                res = -1
                try_run_error_cmd(on_error_cmd)

        con.close()
    else:
        print(database, "not found")
        res = -1
    return res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-path",
        metavar=("DB_PATH"),
        help="Database path (eg: /usr/local/Eaton/IntelligentPowerProtector/db)",
        default="/usr/local/Eaton/IntelligentPowerProtector/db",
    )
    parser.add_argument(
        "--db-filename",
        metavar=("DB_FILENAME"),
        help="Database filename (eg: mc2.db)",
        default="mc2.db",
    )
    parser.add_argument(
        "--on-error-cmd",
        metavar=("ERROR_CMD"),
        help="docker restart ipp",
    )
    args = parser.parse_args(sys.argv[1:])

    return_code = check_ac_status(args.db_path, args.db_filename, args.on_error_cmd)
    sys.exit(return_code)
