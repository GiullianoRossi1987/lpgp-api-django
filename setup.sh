#!/usr/bin/bash
# Copyright (c) 2021 Copyright Holder All Rights Reserved.

function checkIn(){
    ar=(${2// /})
    for i in ${ar[@]}
    do
        if [ $i == $1 ]
        then
            echo true
            break
        else
            continue
        fi
    done
    echo false
}

function setEnv(){
    # MySQL config
    echo "Welcome to the LPGP API setup"
    echo "Insert the IP host for the LPGP official database (leave blank for localhost): "; read MYSQL_LPGP_HOST
    if [ -z $MYSQL_LPGP_HOST ]; then MYSQL_LPGP_HOST="localhost"; fi
    echo "Insert the name of the user for the api (leave blank to root): "; read MYSQL_LPGP_USR
    if [ -z $MYSQL_LPGP_USR ]; then MYSQL_LPGP_USR= "root"; fi
    echo "Insert the password for the user \"$MYSQL_LPGP_USR\": "; read -s MYSQL_LPGP_PASSWD
    if [ ! -z $MYSQL_LPGP_PASSWD ]
    then
        echo "Confirm the password : "; read -s MYSQL_LPGP_PASSWD_C
        if [ $MYSQL_LPGP_PASSWD_C != $MYSQL_LPGP_PASSWD ]
        then
            echo "The passwords doesn't match. Stopping the setup"
            exit -1
        fi
        unset $MYSQL_LPGP_PASSWD_C
    fi
    echo "Insert the path to the downloads control file: "; read SV_CTRL
    if [ -z $SV_CTRL ]; then echo "Invalid download control file "; exit -1; fi
    dbs=$(mysql -h $MYSQL_LPGP_HOST -u $MYSQL_LPGP_USR --password="$MYSQL_LPGP_PASSWD" -e "SHOW DATABASES")
    for i in $dbs; do echo $i; done
    echo "Insert the database in use, the available databases are here above: "; read MYSQL_LPGP_DB
    if [ -z $MYSQL_LPGP_DB ]; then echo "Invalid database"; exit -1; fi

    # Server config
    echo "Insert the hostname of the API server (leave blank to use '0.0.0.0'): "; read SV_HOSTNAME
    if [ -z $SV_HOSTNAME ]; then SV_HOSTNAME="0.0.0.0"; fi

    echo "Insert the port to the server (leave blank for 8080)"; read SV_PORT
    if [ -z $SV_PORT ]; then SV_PORT=8080; fi

    echo "Indexing the configurations..."
    if [ ! -f "config.json" ]; then touch config.json; fi
    # encodes the password
    if [ ! -z $MYSQL_LPGP_PASSWD ]
    then
        mkdir /tmp/lpgp
        echo $MYSQL_LPGP_PASSWD | tee /tmp/lpgp/mysql_passwd >> /dev/null
        enc=$(base64 /tmp/lpgp/mysql_passwd)
        rm -rf /tmp/lpgp
    else
        enc=""
    fi



    # loads the app path and the logs
    APP_PATH=$(pwd)
    LPGP_LOGS="$APP_PATH/logs/lpgp.log"
    SV_LOGS="$APP_PATH/logs/sv.log"

    # Sets and tee's the content on the configurations file
    content="""
{\n
\t    \"config\": {\n
\t\t        \"lpgp\": {\n
\t\t\t            \"mysql_host\": \"$MYSQL_LPGP_HOST\",\n
\t\t\t           \"mysql_usr\": \"$MYSQL_LPGP_USR\",\n
\t\t\t            \"mysql_db\": \"$MYSQL_LPGP_DB\",\n
\t\t\t            \"mysql_passwd\": \"$enc\"\n
\t\t        },\n
\t\t        \"server\": {\n
\t\t\t            \"hostname\": \"$SV_HOSTNAME\",\n
\t\t\t            \"port\": $SV_PORT\n
\t\t        },\n
\t\t        \"env\": {\n
\t\t\t            \"app_path\": \"$APP_PATH\",\n
\t\t\t            \"lpgp_logs\": \"$LPGP_LOGS\", \n
\t\t\t            \"sv_logs\": \"$SV_LOGS\"\n
\t\t        },\n
\t\t        \"controllers\": {\n
\t\t\t           \"control_path\": \"$SV_CTRL\", \n
\t\t        }
}
\t    }\n
}
    """
    if [ ! -f $LPGP_LOGS ]; then touch $LPGP_LOGS; fi
    if [ ! -f $SV_LOGS ]; then touch $SV_LOGS; fi
    echo -en $content | tee config.json >> /dev/null
}

# program itself
if [ ! -f "config.json" ] || [ ! -d "logs" ]
then
    # No server configurations setted
    setEnv
else
    echo "The configurations of the project are setted already"; exit 0
fi
