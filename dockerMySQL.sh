#!/bin/bash

docker run \
   --name test-mysql \
   -e MYSQL_ROOT_PASSWORD=password \
   -p 3307:3306 \
   -v /Users/lingzhang.jiang/projects/personal/ascendas/mysql:/docker-entrypoint-initdb.d \
   -d mysql
