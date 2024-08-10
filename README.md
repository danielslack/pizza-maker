# Pizza Maker
sudo docker run --name pizza-maker -p 27017:27017 -d mongo
uvicorn src.app:app --reload
