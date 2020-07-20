#!/bin/zsh

# paste and run in redis folder

rm nodes*
echo "-> starting nodes"
src/redis-server redis.conf& > redis_logs
src/redis-server redis1.conf& > redis_logs
src/redis-server redis2.conf& > redis_logs
src/redis-server redis3.conf& > redis_logs
src/redis-server redis4.conf& > redis_logs
src/redis-server redis5.conf& > redis_logs

echo "-> 6 nodes up and running"
echo "---make cluster---"
src/redis-cli --cluster create 127.0.0.1:9001 127.0.0.1:9006 127.0.0.1:9002 127.0.0.1:9003 127.0.0.1:9004 127.0.0.1:9005 --cluster-replicas 1
