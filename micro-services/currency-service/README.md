# Currency conversion

## Setup Docker
1. Build image:
```
docker build -t currency-service https://github.com/Emythiel/ita23-3semester.git#main:micro-services/currency-service
```

2. Run the image:
```
docker run -it --rm -p {hostport}:5000 currency-service
```
Where `{hostport}` is the port you wish to use on your machine.

## Usage:
API endpoint (GET request):
```
/currency/{currency}/{price}
```
Where `{currency}` is the 3 letter currency (eg. GBP, EUR, DKK etc.), and `{price}` is the price in USD.
