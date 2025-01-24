from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from groq import Groq


client = Groq(
    api_key="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",
)





app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class User(BaseModel):
    email: str
    password: str

class Topic(BaseModel):
    title: str
    content:str

class InputParams(BaseModel):
    topic: str
    tone: str
    length: int
    target_audience: str

class PromptResponse(BaseModel):
    title: str
    content: str
    words: Optional[int] = None
    seo_score: Optional[float] = None
    readability_score: Optional[float] = None



async def mongo_object():
    MONGODB_URL = "mongodb+srv://andrewblaze2719:meIqpKVOHtbVsXuD@cluster0.qx2mh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    client = AsyncIOMotorClient(MONGODB_URL)
    db = client["webathon_db"]  # Database name
    # user_collection = db["user"]
    # topics_collection = db["topics"]

    return db

async def chat_completion(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    return chat_completion.choices[0].message.content


async def generate_from_groq(input_params):
    topic = input_params['topic']
    tone = input_params['tone']
    length = input_params['length']
    target_audience = input_params['target_audience']

    # Construct the prompt with the provided parameters
    prompt = (
        f"Write a {tone} post on {topic} for {target_audience} "
        f"in {length} words or less. Include suitable emojis.\n\n"
        "Please provide the output in the following format:\n"
        "Title: <title>\n"
        "Content: <content>\n"
        "Also dont exceed the characters of title more than 35 characters but make sure that content is at near to the num of words of length"
    )

    # Generate content using the Groq API
    response_content = await chat_completion(prompt)


    # Parse the title and content from the response
    title = None
    content = None

    for line in response_content.split('\n'):
        if line.startswith("Title:"):
            title = line[len("Title:"):].strip()
        elif line.startswith("Content:"):
            content = line[len("Content:"):].strip()

    return title, content

async def get_stats(topic):

    title = topic["title"]
    content = topic["content"]
    prompt = (
        f"Analyze the following topic and provide detailed statistics:\n\n"
        f"Title: {title}\n"
        f"Content: {content}\n\n"
        "The statistics should include:\n"
        "1. Number of words\n"
        "2. SEO score\n"
        "3. Readability score\n the output should be strictly in the following format:\n"
        "Words: <number of words>\n"
        "SEO Score: <SEO score>\n"
        "Readability Score: <readability score> "
    )

    response_content = await chat_completion(prompt)

    # Parse the statistics from the response
    words = None
    seo_score = None
    readability_score = None

    for line in response_content.split('\n'):
        if line.startswith("Words:"):
            words = int(line[len("Words:"):].strip())
        elif line.startswith("SEO Score:"):
            seo_score = float(line[len("SEO Score:"):].strip())
        elif line.startswith("Readability Score:"):
            readability_score = float(line[len("Readability Score:"):].strip())

    return words, seo_score, readability_score



# Routes
@app.post("/generate")
async def generate_content(params: InputParams):

    print("Generating content")
    db = await mongo_object()
    title, content = await generate_from_groq(params.model_dump())
    
    topics_collection = db["topics"]

    # Save the generated content to the database
    topic = {
        "title": title,
        "content": content,
    }

    print("Generating stats...")

    stats = await get_stats(topic)

    result = await topics_collection.insert_one(topic)
    topic["_id"] = str(result.inserted_id)

    return PromptResponse(
        title=title,
        content=content,
        words=stats[0],
        seo_score=stats[1],
        readability_score=stats[2],
    )

@app.get("/topics")
async def get_topics():
    db = await mongo_object()
    topics_collection = db["topics"]
    # explicitly include _id (to convert it) or exclude it, depending on your needs
    cursor = topics_collection.find({}, {"title": 1, "content": 1})  
    topics = await cursor.to_list(length=None)

    # Convert _id to string if it’s in the returned documents
    for t in topics:
        if "_id" in t:
            t["_id"] = str(t["_id"])

    return topics


@app.get("/topics/{topic_id}")
async def get_topic(topic_id: str):
    db = await mongo_object()
    topics_collection = db["topics"]
    topic = await topics_collection.find_one({"_id": topic_id})

    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Convert _id to string
    topic["_id"] = str(topic["_id"])

    return PromptResponse(
        title=topic["title"],
        content=topic["content"],
    )

@app.post("/login")
async def login(user: User):
    db = await mongo_object()
    user_collection = db["user"]

    # Validate user
    user_data = await user_collection.find_one({"email": user.email})
    if not user_data or user_data["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "status_code": 200}


# @app.get("/login", response_class=HTMLResponse)
# async def login_page():
#     return """
#     <html>
#         <head>
#             <title>Login</title>
#         </head>
#         <body>
#             <h1>Login</h1>
#             <form method="POST" action="/login">
#                 <label for="email">Email:</label>
#                 <input type="email" id="email" name="email" required>
#                 <br>
#                 <label for="password">Password:</label>
#                 <input type="password" id="password" name="password" required>
#                 <br>
#                 <button type="submit">Login</button>
#             </form>
#         </body>
#     </html>
#     """


# @app.post("/login")
# async def login(
#     email: str = Form(...), password: str = Form(...), response: Response = None
# ):
#     db = await mongo_object()
#     user_collection = db["user"]

#     # Validate user
#     user_data = await user_collection.find_one({"email": email})
#     if not user_data or user_data["password"] != password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     # Set a cookie or session
#     response = RedirectResponse(url="http://192.168.137.1:5173/", status_code=302)
#     response.set_cookie(key="session_id", value=str(user_data["_id"]))
#     return response


# @app.get("/register", response_class=HTMLResponse)
# async def register_page():
#     return """
#     <html>
#         <head>
#             <title>Register</title>
#         </head>
#         <body>
#             <h1>Register</h1>
#             <form method="POST" action="/register">
#                 <label for="name">Name:</label>
#                 <input type="text" id="name" name="name" required>
#                 <br>
#                 <label for="email">Email:</label>
#                 <input type="email" id="email" name="email" required>
#                 <br>
#                 <label for="password">Password:</label>
#                 <input type="password" id="password" name="password" required>
#                 <br>
#                 <button type="submit">Register</button>
#             </form>
#         </body>
#     </html>
#     """


# @app.post("/register")
# async def register(
#     name: str = Form(...), email: str = Form(...), password: str = Form(...)
# ):
#     db = await mongo_object()
#     user_collection = db["user"]

#     # Check if user already exists
#     existing_user = await user_collection.find_one({"email": email})
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")

#     # Save user to the database
#     user = {"name": name, "email": email, "password": password}
#     await user_collection.insert_one(user)

#     return RedirectResponse(url="/login", status_code=302)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)