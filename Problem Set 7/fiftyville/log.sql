-- Keep a log of any SQL queries you execute as you solve the mystery.
-- SQLite3 database.db to start
--.schema to see the elements
-- For crime_scene_report to narrow it down to the date time and location of the crime.
    SELECT description
        FROM crime_scene_reports
            WHERE year = 2021 AND month = 07 AND day = 28
                AND street = "Humphrey Street";
        --Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
        --Interviews were conducted today with three witnesses who were present at the time
        -- each of their interview transcripts mentions the bakery.
        --Littering took place at 16:36. No known witnesses.

-- Because of interview prompt in previous query now look into interviews.
    SELECT transcript
        FROM interviews
            WHERE year = 2021 AND month = 07 AND day = 28;
        --“Ah,” said he, “I forgot that I had not seen you for some weeks. It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”                                                                                                                               |
        --| “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”                                                                                                                                                                                      |
        --| “You had my note?” he asked with a deep harsh voice and a strongly marked German accent. “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.                                                                                                                   |
        --Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
        --| I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
        --| As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
        --| Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day. My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.

--Look at the car park security footage for cars leaving within 10 minutes of the crime:
    SELECT name
        FROM people
            JOIN bakery_security_logs ON people.license_plate = bakery_security_logs.license_plate
                WHERE year = 2021 AND month = 07 AND day = 28 AND hour = 10 AND minute > 15 AND minute < 25;
        --Current suspects:
            --Vanessa
            --Bruce
            --Barry
            --Luca
            --Sofia
            --Iman
            --Diana
            --Kelsey
-- Look at atm transactions for the morning of the cirme in order to narrow down suspects:
    SELECT people.name
        FROM people
            JOIN bank_accounts ON people.id = bank_accounts.person_id
                JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
                    WHERE atm_transactions.year = 2021 AND atm_transactions.month = 07 AND atm_transactions.day = 28
                        AND atm_transactions.atm_location = "Leggett Street" AND atm_transactions.transaction_type = "withdraw";
        --Current suspects:
        --Bruce
        --Brooke
        --Kenny
        --Iman
        --Luca
        --Taylor
        --Benista
            --Cross Referenced Suspects:
                --Bruce
                --Luca
                --Iman
                --Diana
--Look at phone calls around the time of the crime and link to names.
    SELECT name
        FROM people
            JOIN phone_calls ON people.phone_number = phone_calls.caller
                WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60;
        --Current Suspects:
        --Sofia
        --Kelsey
        --Bruce
        --Kelsey
        --Taylor
        --Diana
        --Carina
        --Kenny
        --Benista
            --Cross referenced suspects
                --Bruce
                --Dianna
--Use first query to find the flight ID for flights out of fiftyville.
--Then Use second query to find out whether bruce or dianna(our two remaining suspects) were on the first flight out of fiftyville the day after the crime was commited.
--Also SELECT destination_airport_id for destination of escape later
SELECT * FROM airports WHERE city = "Fiftyville";
SELECT people.name, flights.hour, flights.minute, destination_airport_id
    FROM people
        JOIN passengers ON people.passport_number = passengers.passport_number
            JOIN flights ON passengers.flight_id = flights.id
                JOIN airports ON flights.origin_airport_id = airports.id
                    WHERE airports.id = 8 AND flights.year = 2021 AND flights.month = 07 AND flights.day = 29 AND flights.hour = 8
                        AND people.name = "Bruce" OR people.name = "Dianna";
--Now we know it was Bruce on the flight go back and find out who he called to book the flight.
--First we need to find out Bruce's Phone Number to create a condition for the final query.
SELECT name, caller
        FROM people
            JOIN phone_calls ON people.phone_number = phone_calls.caller
                WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60;
--Now we can run the final query
SELECT name
    FROM people
        JOIN phone_calls ON people.phone_number = phone_calls.receiver
            WHERE year = 2021 AND month = 07 AND day = 28 AND duration < 60
                AND caller = "(367) 555-5533";

--Find out where the person escaped to
SELECT city
    FROM airports
        JOIN flights ON airports.id = flights.destination_airport_id
            WHERE flights.destination_airport_id = 4;






sqlite> create table foo(a, b);
sqlite> .mode csv
sqlite> .import test.csv foo
