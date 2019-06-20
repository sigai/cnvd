from redis import Redis

r = Redis(decode_responses=True)

for i in range(0, 18768, 20):
    r.sadd("cnvd:offset", i)
