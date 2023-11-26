#!/bin/sh

# Twitter Sink
echo "Starting Twitter Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "twittersink",
  "config":{
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "twittersink",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.twittersink.kafkapipeline.twitterdata.mapping": "location=value.location, tweet_date=value.datetime, tweet=value.tweet, classification=value.classification",
    "topic.twittersink.kafkapipeline.twitterdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'

# OpenWeather Sink
echo "Starting Weather Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "weathersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "weather",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.weather.kafkapipeline.weatherreport.mapping": "location=value.location, forecastdate=value.report_time, description=value.description, temp=value.temp, feels_like=value.feels_like, temp_min=value.temp_min, temp_max=value.temp_max, pressure=value.pressure, humidity=value.humidity, wind=value.wind, sunrise=value.sunrise, sunset=value.sunset",
    "topic.weather.kafkapipeline.weatherreport.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."

# FakerAPI Sink
echo "Starting Faker Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "fakersink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "faker",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.faker.kafkapipeline.fakerdata.mapping": "id=value.id, street=value.street, streetname=value.streetName, buildingnumber=value.buildingNumber, city=value.city, zipcode=value.zipcode, country=value.country, country_code=value.country_code, latitude=value.latitude, longitude=value.longitude",
    "topic.faker.kafkapipeline.fakerdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."

# IQAir Sink
echo "Starting IQAir Sink"
curl -s \
     -X POST http://localhost:8083/connectors \
     -H "Content-Type: application/json" \
     -d '{
  "name": "iqairsink",
  "config": {
    "connector.class": "com.datastax.oss.kafka.sink.CassandraSinkConnector",
    "value.converter": "org.apache.kafka.connect.json.JsonConverter",
    "value.converter.schemas.enable": "false",  
    "key.converter": "org.apache.kafka.connect.json.JsonConverter",
    "key.converter.schemas.enable":"false",
    "tasks.max": "10",
    "topics": "iqair",
    "contactPoints": "cassandradb",
    "loadBalancing.localDc": "datacenter1",
    "topic.iqair.kafkapipeline.iqairdata.mapping": "city=value.city, state=value.state, country=value.country, latitude=value.latitude, longitude=value.longitude, current_ts=value.current_ts, current_pollution_aqius=value.current_pollution_aqius, current_pollution_mainus=value.current_pollution_mainus, current_pollution_aqicn=value.current_pollution_aqicn, current_pollution_maincn=value.current_pollution_maincn, current_weather_tp=value.current_weather_tp, current_weather_pr=value.current_weather_pr, current_weather_hu=value.current_weather_hu, current_weather_ws=value.current_weather_ws, current_weather_wd=value.current_weather_wd, current_weather_ic=value.current_weather_ic",
    "topic.iqair.kafkapipeline.iqairdata.consistencyLevel": "LOCAL_QUORUM"
  }
}'
echo "Done."
