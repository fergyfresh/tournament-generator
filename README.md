# Tournament Generator
This project provides a Python module that uses a PostgreSQL database to keep
track of players and matches in a game tournament, using the Swiss pairing
system.

### How to run

This directory can be initiated with [Vagrant](https://www.vagrantup.com/)
by executing the command `vagrant up` within the `vagrant/` directory.  The
test cases can be run by executing the following commands:

- `vagrant up` sets up database with pg_config.sh script (see Vagrantfile and docs)
- `vagrant ssh`
- `cd /vagrant/tournament`
- `python tournament_test.py`

- `psql -f /vagrant/tournament/tournament.sql` creates the database and tables

*Note after you `vagrant ssh` you will not be able to see the
`/vagrant/tournament` path but you can cd there!
