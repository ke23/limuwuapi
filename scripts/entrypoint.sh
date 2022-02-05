#!/bin/sh

set -e # exit if errors happen anywhere

if [ "$DB_NAME" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 1
    done

    echo "PostgreSQL started"
fi

sed -i -e 's/w3-table-all/ws-table-all/g' /usr/local/lib/python3.9/site-packages/fake_useragent/utils.py

python manage.py collectstatic --noinput --settings=limuwuapi.settings.prod
# python manage.py migrate --settings=limuwuapi.settings.prod
exec "$@"
# gunicorn --socket :8000 --master --enable-threads --module mysite.wsgi