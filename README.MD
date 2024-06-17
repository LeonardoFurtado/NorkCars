

# Build project

```
docker-compose up --build
```

---

# Tests

Just run
```
docker exec -it norkcars_web_1 pytest
```

where norkcars_web_1 is the container name.

to avoid run containers you can use pipenv:

```
pipenv shell
pipenv install
pytest
```
the postgresql is not necessary to run the tests.

# Auth

**POST** /register

Body example:

```json
{
  "username": "example",
  "password": "example"}
```

**POST** /login

Body example:

```json
{
  "username": "example",
  "password": "example"}
```

after that you will receive a token like this:

```json
{
	"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxODU4NDYzMSwianRpIjoiNGYxMzE4MmItZmI2NS00YzQ5LWIxMWQtMTJjNTQ0ZjBlMGNiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6InNybGVvbmFyZG8ifSwibmJmIjoxNzE4NTg0NjMxLCJjc3JmIjoiYTE0MGQwMDEtNzFkZi00ZTIzLThiYTItZjczNWZhMTJlNzdjIiwiZXhwIjoxNzE4NTg1NTMxfQ.JVh8mVVBRY1rta66dQHNeZVK3YvQeY5PYMjSdeLmzuY"
}
```
you will need to use this format of token to access the routes

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxODU4NDYzMSwianRpIjoiNGYxMzE4MmItZmI2NS00YzQ5LWIxMWQtMTJjNTQ0ZjBlMGNiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6InNybGVvbmFyZG8ifSwibmJmIjoxNzE4NTg0NjMxLCJjc3JmIjoiYTE0MGQwMDEtNzFkZi00ZTIzLThiYTItZjczNWZhMTJlNzdjIiwiZXhwIjoxNzE4NTg1NTMxfQ.JVh8mVVBRY1rta66dQHNeZVK3YvQeY5PYMjSdeLmzuY
```

---

# API DOC

## Owners

**POST** /owners

> create a new owner

Body example:

```json
{
  "name": "Harry Potter"
}
```

---

**GET** /owners

> retrieve all owners

---

**GET** /owners/<owner_id>

> retrieve an owner by id

---

**PATCH** /owners/{owner_id}

> update an owner

Body:

```json
{
  "name": "Sirius Black"
}
```

---

**DELETE** /owners/{owner_id}

> delete an owner

## Cars

**POST** /cars

> create a new car

Body example:

colors should be yellow, blue or gray.
models should be hatch, sedan or convertible.

```json
{
  "color": "yellow", 
  "model": "sedan",
  "owner_id": 1
}
```

---

**GET** /cars

> retrieve all cars

---

**GET** /owners/<owner_id>/cars

> retrieve all cars from an owner

---

**GET** /cars/{car_id}

> retrieve a single car

---

**PATCH** /cars/{car_id}

> update a single car

Body example:

```json
{
  "color": "yellow",
  "model": "sedan"
}
```

--- 
DELETE /cars/{car_id}

> delete a single car