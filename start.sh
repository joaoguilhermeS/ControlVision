docker swarm leave --force
docker swarm init --advertise-addr 192.168.146.164
docker stack deploy -c ./container/compose.yml stack
# docker service logs prometheus_mysql -f
# docker service update --force prometheus_mysql
# sudo chown -R 999:999 mysql-data/
# docker service logs prometheus_mysql --no-trunc
# docker service inspect --pretty [SERVICE_NAME]
# mysql -u root -p ControlVision < /docker-entrypoint-initdb.d/init-db.sql
# mysql -u root -p ControlVision
# GRANT ALL PRIVILEGES ON ControlVision.* TO 'root'@'10.0.1.4' IDENTIFIED BY 'A06£6cG@tp.*'; FLUSH PRIVILEGES;
