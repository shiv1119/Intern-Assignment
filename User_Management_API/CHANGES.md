# Code Refactoring Challenge

## Getting Started

### Prerequisites
- Python 3.8+ installed
- 3 hours of uninterrupted time

### Setup (Should take < 5 minutes)
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd User_Management_API #(messy-migration) 

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

# To run test cases
pytest #(Recommended)

### Important Note - One test case will fails as it will check for week passwords. Input will be password that does not strong So it will fail. Actually Which means it passed.

# Start the application
python app.py 
#or 
flask --app app run --port=5000 

# The API will be available at http://localhost:5000
```

### Post Man API Test collection link  (Run server and open the collection and send requests to server to get responses)- https://interstellar-resonance-436052.postman.co/workspace/Career-Booklet-profile-manageme~8ed84786-d16e-47b4-a71a-b4d619bcd29b/collection/33641353-c8a8a582-5c88-47c6-a458-d5409d893c64?action=share&creator=33641353

### Testing the Application
The application provides these endpoints:
- `GET /` - Health check
- `GET /users` - Get all users
- `GET /user/<id>` - Get specific user
- `POST /users` - Create new user
- `PUT /user/<id>` - Update user
- `DELETE /user/<id>` - Delete user
- `GET /search?name=<name>` - Search users by name
- `POST /login` - User login


### Critical Issues Identified By Priority and its concerns explained

1. **No Password Hashing** - There was no password hashing. Saving plain text as password is most dangerous.

2. **Returning Password while getting all user lists** - While getting all users it was also returning passwords. Which is dangerous.

3. **No Password validation** - Password validation was not there. Passwords can be created with any test like abc, 1, 123 etc. which is again raise concern.

4. **No Unique Email Constraint** - There was no uniqueness in saving email to database. A user was able to create unlimited account with same email.

5. **SQL Injection Prevention** - cursor.execute(f"SELECT * FROM users WHERE email = '{email}'") here SQL queries were constructed using string interpolation which raises concern for sql injection.

6. **Improper Response Format** - The given formats was returning tuples or raw messages.

7. **Modularity and Error Handling** - There was no error handling and modularity.

8. **No pagination** - Get all user routes fetches all the user at once is fine for small projects. But suppose million users. Fetching all at once will make server like cry.

9. **No Tests** - No test to ensure the working functionality of the project.

### What implemented to resolve critical issues

1. **Implemented Bcrypt Hashing** - Used bcrypt to securely hash the password before storing them in database. Even if database is compromised, password remain protected.

2. **Removed Password Field from Response** - Modified select queries to fetch only non sensitive data which prevents accidental exposure of hashed or lets say plain password if hashing not implemented.

3. **Added Strong Password Checker** - Integrated a password strength checker ensuring minimum length, numbers, uppercase, lowercase, and special characters. Which ensures strong security standards for an account creation.

4. **Added Uniqueness Check** - Added unique constraint and also checked that if users with email already exists then abort creations of account.

5. **Used Parameterized Queries** - Replaced all dynamic SQL with parameterized queries using ? placeholders.

6. **Response Format - Standard JSON Responses with Proper Status code and messages or errors** - All endpoints now return well-structured JSON with status, message, and data.

7. **Added Modular Blueprints & Centralized Error Handlers** - Separated user and auth logic into blueprints, and added utils/errors.py for consistent error handling.

8. ** Implemented Limit & Offset (Pagination)** -  Added pagination in GET /users using limit and offset query params. Which will surely increase performance of the api.

9. **Added Unit Tests** - Added unit tests to ensure code reliability.


### Justification for Architectural Decisions

1. **Factory Pattern** - Its helps to make the app more testable and configurable, especially useful for testing with an in memory SQLits DB.

2. **Blueprints** - This promotes separation by grouping related routes and logic together like (User routes, auth routes, and utility functions etc.)

3. **Bcrypt for Hashing** - Industry standard for secure password storage due to its salt and computational cost features.

4. **Parameterized Queries**  - To ensure prevention against SQL injection.

5. **Testing with Fixtures** - This helps to create an isolated environments per test. Reducing dependencies and making debugging easier.

### Some of the trade-offs Made

1. **SQLite** - If it was production based then there was a lot of limitations like concurrency but for this project it was used for simplicity amd ease of testing.

2. **No JWT For Login** - Simple login system (email-password) for clarity and to keep scope focused. But this sacrifices session scalability and stateless authentication which JWT can offer.

3. **Basic Password Validation** - Instead of integrating a 3rd party library like zxcvbn, i implemented custom regex-based validation for simplicity.

4. **Limited Pagination** - Pagination has been implemented using basic limit and offset without total count or next/prev links for simplicity, which could be improved for richer APIs.

### AI Usage

Chatgpt - 
1) Most important, I was from Fast API and Django background. As it was instructed to do in Flask. So I used it a road map to learn Basic of Flask within one day and kept next day for development of the project because I got enough time.

2) For writing password validation function and some tests.



