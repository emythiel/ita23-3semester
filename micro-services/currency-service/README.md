# Currency conversion

## Setup Docker
1. Build image:
```
docker build -t currency-service https://github.com/Emythiel/ita23-3semester.git#main:micro-services/currency-service
```

2. Run the image:
```
docker run -it --rm -p 5420:5420 currency-service
```

## Usage:
API endpoint (GET request):
```
/currency/{currency}/{price}
```
Where `{currency}` is the 3 letter currency (eg. GBP, EUR, DKK etc.), and `{price}` is the price in USD.
