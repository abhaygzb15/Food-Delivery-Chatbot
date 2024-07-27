# Food Delivery Chatbot

## About

The Food Delivery Chatbot is a conversational agent designed to enhance user interaction for food delivery services. It integrates with Dialogflow for natural language processing and utilizes a FastAPI backend to manage orders with a MySQL database. Users can place new orders, add or remove items, track order status, and receive real-time updates through a web interface.

<p align="center">
  <img src="https://github.com/user-attachments/assets/3667e414-5362-43af-aef5-91b5f6a0a6a2" width="300" />
  <img src="https://github.com/user-attachments/assets/d54615fe-9fe6-447c-9db8-7c1ef701bd04" width="300" />
  <img src="https://github.com/user-attachments/assets/7c83bd2c-6fb2-47fc-94e1-1d7844f49c67" width="300" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/8e367fb7-f490-4d8b-a3d8-f8b33dc376b5" width="300" />
  <img src="https://github.com/user-attachments/assets/e14ba4ce-b8aa-44fa-9e74-ec43930fff6c" width="300" />
  <img src="https://github.com/user-attachments/assets/b86894c6-fbec-420d-946e-3b1651d27bb0" width="300" />
</p>

## Technologies Used

- **Dialogflow**: For natural language understanding and chatbot capabilities.
- **FastAPI**: For building the backend API to handle chatbot requests.
- **MySQL**: For managing order data and tracking.
- **HTML/CSS**: For creating the front-end web interface.

## How to Use and Integrate

### 1. Set Up the Backend

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/food-delivery-chatbot.git
    cd food-delivery-chatbot
    ```

2. **Install Dependencies:**

    ```bash
    pip install fastapi uvicorn mysql-connector-python
    ```

3. **Configure the Database:**

    Ensure MySQL is running, and create the database `pandeyji_eatery`. Set up the necessary database schema and stored procedures.

4. **Run the Server:**

    ```bash
    uvicorn main:app --reload
    ```

### 2. Integrate with Dialogflow

1. **Create Intents and Contexts:**

    Follow the video tutorial linked below to create the necessary intents and contexts in Dialogflow:  
    [Video Tutorial](https://youtu.be/2e5pQqBvGco?si=GM7_rEKCmVRxlwM9)

2. **Update Dialogflow Integration:**

    Ensure that the Dialogflow agent is correctly integrated with your FastAPI backend.

### 3. Set Up the Frontend

1. **Serve the HTML File:**

    Open `website.html` in your web browser. Ensure that it is correctly linked to `styles.css` and images.

2. **Embed the Chatbot:**

    The chatbot is embedded via an iframe. Update the `src` attribute of the iframe with the correct Dialogflow demo URL.
