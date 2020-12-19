<H1>IS-601 Final Team Project</H1>
<H1>Gas Mileage History Website</H1>
<H2>by Jeril Jose, Andrew Drumm and William Herman</H2>

<H2>Features and Credits</H2>
<H3>1: Login - by Jeril Jose</H3>

- Create table for users
- Id
- Email
- password(hash)
- First_name
- Last_name
- Verification_token
- Is_verified
- is_admin

- Landing Page
- Plain HTML page with links to signup and login
- Signup
- Jinja page
- Python logic for signup
- Email verification
- Sendgrid/ gmail server
- Generate token and email the verification url to user
- Login
- Jinja Page
- Python logic for login


<H3>User Home Page - after login - by Andrew Drumm</H3>

- Gas Mileage statistics 
- Create an sql gas table 
- Date purchased input
- Gallons of gas input
- Purchase price input
- Miles driven input
- MPG calculated(Jeril Jose)

- List all records, Add record, edit record, view record
- Jinja pages
- Python logic
- Misc



<H3>Admin Page - by William Herman</H3>

- Admin should be able to edit/delete user
- Admin should be able to edit/delete gas info

- Create an admin page
- List of users
- Option to edit/delete/view each user
- When clicked on view admin can see gas information for that user
- View page should let the admin edit/delete gas info

<H2>Installation Instructions for Using the App with Docker</H2>

