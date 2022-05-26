To connect to the running trino CLI
```bash
$ docker-compose exec trino-coordinator trino
```
To load running postgresql by dump execte the following query
```bash
$ psql --host=localhost --username=configured-username --dbname=configured-dbname --password < dump.sql
```
To show awailable trino catalogs execute the following query
```bash
[trino> show catalogs;
```
To show all schemas inside the catalog execute
```bash
[trino> show schemas in <catalog_name>;
```
To list all available tables
```bash
[trino> show tables from postgresql.public;
```
To list available tables execute the following query
```bash
[trino> describe postgresql.public.accounts;
```
For example to query data with joint in postgresql catalog execute the next query. (WARNING: Ensure the dump was loaded properly!)
```bash
[trino> SELECT accounts.user_id FROM postgresql.public.accounts AS accounts INNER JOIN postgresql.public.tickets AS tickets ON accounts.user_id=tickets.user_id;
```