#!/bin/bash

# Weboldal azonosítok lekérése
WEBSITE=$(redis-cli keys "webpage:*")

# Ellenőrzési idő
INTERVAL=60

# Email beállítások
EMAIL_SUBJECT="A Weboldal nem elérhető"
LOGFILE="/var/log/websiteCh.log"

