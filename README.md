Django Student Recruitment Platform
This project is a student recruitment platform developed using Django, a high-level Python web framework. The platform allows students to register, login, create profiles, upload documents, search for jobs, and interact with recruiters. Recruiters can post job listings, review student applications, and accept/reject applicants.

Features
User Registration and Authentication:

Students can register with their details including name, email, phone, date of birth, address, gender, course, and college.
Recruiters can register with their company details including name  and other contact information.
User authentication is implemented using Django's built-in authentication system.
Passwords are securely stored using the bcrypt hashing algorithm.
User Profiles:

Students can view and edit their profiles, which display their personal information and uploaded documents.
Recruiters have access to their company profile and can update their information.
Document Uploads:

Students can upload documents related to their education, such as transcripts or certificates.
Uploaded documents are associated with the student's profile and can be viewed by recruiters.
Job Listings and Search:

Recruiters can post job listings with details such as title, description, category, requirements, duration, and budget.
Students can search for jobs using keywords and job categories.
Pagination is implemented to display a limited number of job listings per page.
Job Application and Review:

Students can apply for jobs by sending messages to recruiters, expressing their interest and providing additional information.
Recruiters can review job applications, accept or reject applicants, and send notifications to students.
Accepted applicants are notified and can view the status of their applications.
Forgot Password Functionality:

Users can request a password reset if they forget their passwords.
An email with a new randomly generated password is sent to the user's registered email address.
Change Password:

Users can change their passwords by providing their current password and a new password.


Technologies Used
Python
Django
HTML/CSS
JavaScript
MYSQL

Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.
