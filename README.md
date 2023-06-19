Локально:

docker build -t mysmster/duellio .
docker login -u mysmster
docker push mysmster/duellio

На сервере
docker login -u mysmster
docker pull mysmster/duellio
docker run -p 8000:8000 mysmster/duellio


