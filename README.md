# webathon
# Automated Content Generation using AI

## Overview

Automated Content Generation is a platform that allows users to effortlessly create high-quality content using AI. By providing a brief input (such as a topic, tone, maximum length, and target audience), users can generate tailored content with the help of advanced language models like LLaMA. The backend processes the user's request using the Groq API to interact with the LLM, parses the response via FastAPI, and sends the generated content back to the frontend as a structured JSON object containing the `title` and `content`.

---

## Features

- **AI-Powered Content Generation**  
  Users can generate content by submitting minimal input parameters (e.g., topic, tone, max length, target audience).
  
- **Content Management**  
  Users can:
  - View generated content in a structured format.
  - Regenerate or modify the content based on their preferences.
  - Save content to their personal content history.

- **User Authentication**  
  - Secure user registration and login system.
  - Each user’s data is linked to their unique account.

- **Database Functionality**  
  - Content is stored in MongoDB Atlas in the cloud.
  - Each user's content is tied to their user ID.
  - Each content entry is stored as a document containing fields like `topic_id`, `title`, and `content`.

- **Frontend Interface**  
  - Built using React with Vite for a fast and responsive user experience.
  - Displays content in a clean and user-friendly format.

---

## Tech Stack

- **Frontend:**  
  - React + Vite  
  - Deployed on **Vercel** for scalability and performance.

- **Backend:**  
  - FastAPI (Python) to handle API requests and parse AI-generated responses.  
  - Deployed on **AWS** for reliable cloud hosting.  

- **AI Integration:**  
  - Groq API for communication with the LLaMA language model.  

- **Database:**  
  - **MongoDB Atlas** for secure and cloud-based data storage.

---

## Workflow

1. **User Input:**  
   The user provides input parameters (topic, tone, etc.) in the frontend interface.

2. **Request Handling:**  
   - The input is sent to the backend via FastAPI.  
   - FastAPI communicates with the LLaMA model through the Groq API.  
   - The AI generates a response based on the user input.

3. **Content Generation:**  
   - The backend processes and parses the AI-generated response.  
   - The response is returned to the frontend as a JSON object containing the `title` and `content`.

4. **Content Management:**  
   - Users can view, regenerate, or modify the content.  
   - All generated content is stored in MongoDB Atlas, tied to the user’s account.

---

## Key Functionalities

- **Registration and Login:**  
  Secure authentication ensures that each user has access to their own content history.

- **Content History:**  
  Users can view their past generated content, regenerate it, or customize it further.

- **Seamless Frontend-Backend Communication:**  
  The backend efficiently handles AI communication and returns structured responses to the frontend.

---

This project demonstrates a practical application of AI in automating content creation, with a focus on user customization, scalability, and performance.

## Dev Docs

### FastAPI Endpoints

#### 1. User Authentication

- **Register User**
    - **Endpoint:** `/register`
    - **Method:** `POST`
    - **Description:** Registers a new user with a unique username and password.
    - **Request Body:**
        ```json
        {
            "username": "string",
            "password": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "message": "User registered successfully",
            "user_id": "string"
        }
        ```

- **Login User**
    - **Endpoint:** `/login`
    - **Method:** `POST`
    - **Description:** Authenticates a user and returns a JWT token.
    - **Request Body:**
        ```json
        {
            "username": "string",
            "password": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "token": "string"
        }
        ```

#### 2. Content Generation

- **Generate Content**
    - **Endpoint:** `/generate`
    - **Method:** `POST`
    - **Description:** Generates content based on user input parameters.
    - **Request Body:**
        ```json
        {
            "topic": "string",
            "tone": "string",
            "max_length": "integer",
            "target_audience": "string"
        }
        ```
    - **Response:**
        ```json
        {
            "title": "string",
            "content": "string"
        }
        ```

#### 3. Content Management

- **Get Content History**
    - **Endpoint:** `/topics`
    - **Method:** `GET`
    - **Description:** Retrieves the content history for the authenticated user.
    - **Headers:**
        ```json
        {
            "Authorization": "Bearer <token>"
        }
        ```
    - **Response:**
        ```json
        [
            {
                "topic_id": "string",
                "title": "string",
                "content": "string"
            },
            ...
        ]
        ```

### Usage

1. **Register a new user** by sending a POST request to `/register` with the required username and password.
2. **Login** using the `/login` endpoint to receive a JWT token.
3. **Generate content** by sending a POST request to `/generate` with the desired input parameters.
4. **manage content** Using `/topic` api . refer main.py code.

## Running the Backend

1. **Install Dependencies**  
   Use the following command to install all the required dependencies from `requirements.txt`:
   ```bash
   pip install -r requirements.txt
