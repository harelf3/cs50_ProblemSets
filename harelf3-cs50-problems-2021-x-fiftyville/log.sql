-- Keep a log of any SQL queries you execute as you solve the mystery.
-- see if the thief got any money
SELECT name FROM people WHERE id IN  (SELECT person_id FROM bank_accounts WHERE creation_year =2020)
-- SUSES Sara Charlotte David Amy
SELECT name FROM people WHERE id IN  (SELECT id FROM phone_calls WHERE day = 28 and month = 7 and year = 2020)
-- see the crime scence reports -- see when robberay was
SELECT * FROM crime_scene_reports WHERE street = 'Chamberlin Street'
-- see the interview
SELECT * FROM interviews WHERE(year = 2020 and month = 7 and day =28)
-- check atm
SELECT name,atm_transactions.transaction_type FROM people
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE year = 2020 and month = 7 and day =28 and atm_location ='Fifer Street'
-- check phone calls
SELECT * FROM phone_calls

SELECT receiver FROM people
JOIN phone_calls ON phone_calls.receiver = people.name
WHERE year = 2020 and month = 7 and day =28 and duration <61
SELECT name FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE year = 2020 and month = 7 and day =28 and duration <61)

-- CHECK COURT HOUSE
SELECT name,courthouse_security_logs.minute ,courthouse_security_logs.hour from people
JOIN courthouse_security_logs ON courthouse_security_logs.license_plate = people.license_plate
WHERE year = 2020 and month = 7 and day =28 and hour =10  and activity = 'exit' ORDER BY name

SELECT name from people WHERE license_plate IN (SELECT courthouse_security_logs.license_plate FROM courthouse_security_logs WHERE (year = 2020 and month = 7 and day =28 and hour =10 and minute = 25 and activity = 'exit'))

-- check first flight
SELECT * FROM airports WHERE id = (SELECT * FROM flights where year = 2020 and month = 7 and day =29 and origin_airport_id = 8 ORDER BY hour )


SELECT name FROM people
JOIN flights ON passengers.flight_id = flights.id
JOIN passengers ON people.passport_number = passengers.passport_number
WHERE flights.id  =36 

-- CHECK WHO CALLED WH0 
SELECT caller, receiver FROM phone_calls

WHERE year = 2020 and month = 7 and day =28 and duration <61 
