#!/bin/bash

# Weboldalak azonosítóinak lekérése Redis-ből
WEBSITES=$(redis-cli keys "webpage:*")

# Email küldés beállításai
EMAIL_SUBJECT="Weboldal elérhetetlenség figyelmeztetés"
LOGFILE="/var/log/website_checker.log"

# Funkció a naplózáshoz
log_message() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOGFILE
}

# Weboldal elérhetőségének ellenőrzése
check_website() {
  local id=$1
  local url=$(redis-cli hget $id "url")
  local email=$(redis-cli hget $id "email")
  local current_status=$(redis-cli hget $id "status")

  # Küldünk egy HTTP kérést és lekérjük az állapotkódot
  local status_code=$(curl -o /dev/null -s -w "%{http_code}\n" $url)

  # Az új állapot meghatározása
  local new_status="offline"
  if [ "$status_code" -eq 200 ]; then
    new_status="online"
    #Ki kell ezt majd törölni
    echo "$url elérhető!"
  fi

  # Ha az állapot megváltozott, frissítsük a Redis-ben és küldjünk értesítést
  if [ "$new_status" != "$current_status" ]; then
    redis-cli hset $id "status" "$new_status"
    log_message "A(z) $url állapota megváltozott: $current_status → $new_status"

    # Ha offline lett, küldjünk emailt
    if [ "$new_status" == "offline" ]; then
      echo "A(z) $url weboldal jelenleg nem elérhető." | mail -s "$EMAIL_SUBJECT" $email
      log_message "Értesítés küldve a következő címre: $email"
    fi
  fi
}

# Végigmegyünk az összes weboldalon
for website_id in $WEBSITES
do
  check_website $website_id
done