VERSION=$1
TOKEN=$2

docker pull slawiko/candidata_bot:$VERSION

docker stop candidata_bot || true

docker run --rm -d --name candidata_bot slawiko/candidata_bot:$VERSION $TOKEN