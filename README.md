# healthcarechatbot
A Python-based healthcare chatbot that predicts diseases from symptoms, suggests precautions, shows symptom descriptions, and recommends doctors with appointment links. Built with machine learning and Tkinter for an interactive, user-friendly experience.

This project aims to address this need by developing a healthcare chatbot that utilizes a Decision Tree Classification algorithm for disease prediction based on user-reported symptoms. Additionally, the system incorporates Google search integration to recommend relevant doctors or specialists for further consultation. Built using Python, Tkinter, and medical datasets, this chatbot is designed to assist users in making informed health decisions efficiently and interactively.

![image](https://github.com/user-attachments/assets/bb1ae9e0-7559-4035-9a2e-6711967f730d)

Healthcare Chatbot Using Decision Tree Classification
The advancement of artificial intelligence (AI) and machine learning (ML) has greatly contributed to the development of intelligent systems that enhance the accessibility and quality of healthcare. One such innovation is the healthcare chatbot, a software system that simulates human conversation to interact with patients and provide preliminary medical support. In this section, we focus on a healthcare chatbot developed using the Decision Tree Classification algorithm, which is particularly effective for symptom-based disease prediction.
The chatbot typically consists of:
● User Interface: Developed using tools like Tkinter (Python GUI library) to allow users to enter symptoms interactively.
● Machine Learning Model: A Decision Tree Classifier trained on a dataset containing various symptoms and corresponding diseases.
● Output Module: Displays the predicted disease and suggests relevant precautions and doctor recommendations through hyperlinks (e.g., Google search links).

![image](https://github.com/user-attachments/assets/f0806545-ee69-4864-914a-49a3322073b4)

The GUI components were built using Tkinter, a Python library widely used for creating simple and interactive desktop applications. The structure of the GUI development was divided into three major parts: Login Page, Registration Page, and Question Dialog Box.
Login Page
The Login Page serves as the first interaction point between the user and the chatbot system. It was designed to authenticate existing users securely. 
 Purpose: To allow users who have already registered to log in to their account and access the chatbot.
 Functionality:
- The system verifies user credentials against the stored records.
- If login credentials are correct, users are redirected to the chatbot interface.
- If login fails, an error message is displayed.
 Design:
- A simple form asking for Username and Password.
- A Login button to verify the entered credentials.
- A "Register Here" link/button redirecting to the registration page for new user.
![image](https://github.com/user-attachments/assets/9d9e8efd-8b88-4057-8534-ab59a6c6cacc)

Register Page
The Registration Page is designed for new users to create their accounts.
 Purpose: To allow first-time users to register and securely store their login details for future access.
 Functionality:
- Validates that all required fields are filled.
- To Check if the username already exists.
- If registration is successful, user details are stored in the local database or a file, and a success message is displayed.
 Design:
- A simple form asking for Choose Username and Choose
Password.
- A Register button to submit the registration form

  ![image](https://github.com/user-attachments/assets/2ada9fb0-981e-4fb6-8bb8-247e9d427acb)

Question Dialog Box
After logging in, users engage with the chatbot via a Question Dialog Box.
 Purpose: To gather user symptoms and facilitate a conversational flow for disease prediction.
 Functionality:
- The chatbot asks users about their symptoms one by one.
- Users simply click YES or No to response.
- Based on the inputs, the chatbot processes the data and predicts possible diseases.
- At the end, it recommends a doctor based on the predicted disease.
 Design:
- A text entry box where users can input symptoms or respond to chatbot queries.
- A start button to start the process.
- A display area where both user inputs and chatbot responses are shown in a conversation-like format.

  ![image](https://github.com/user-attachments/assets/eadba2b2-fbbf-4894-84c5-b379af21dd1b)
  ![image](https://github.com/user-attachments/assets/0e8dde03-9296-4f0b-8aa6-d6e39b3724b7)
  ![image](https://github.com/user-attachments/assets/dca460a8-5f4f-4541-9a69-6f0b148346cc)
  ![image](https://github.com/user-attachments/assets/7c909832-0eb5-427a-90da-383c88757244)

  Results
  ![image](https://github.com/user-attachments/assets/7d49afbc-6990-40ea-af92-64dd9e44402c)



