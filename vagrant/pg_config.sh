
apt-get -qqy update
apt-get -qqy install postgresql python-psycopg2
apt-get -qqy install python-flask python-sqlalchemy
apt-get -qqy install python-pip
pip install bleach
su postgres -c 'createuser -dRS vagrant'
su vagrant -c 'psql -f /vagrant/tournament/tournament.sql'
