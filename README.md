This operates as a proxy server for the Bryant Evolution thermostat, capturing data and sending it to an InfluxDB time-series database (https://www.influxdata.com/time-series-platform/influxdb/)

```
docker run -d -p 8080:8080 --restart=always --name bryant -e INFLUXHOST=<influxdb_host> -e INFLUXPORT=8086 -e INFLUXUSER=admin -e INFLUXPASS=admin -e INFLUXDB=bryant   bryant thecase/bryant-influx
Reconfigure your thermostat to use the IP:port of your new proxy server:
```

`menu -> wireless -> advanced -> manage proxy servers`
